from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn import linear_model, datasets
from sklearn import metrics
from sklearn.linear_model import SGDClassifier
import pandas as pd

# df = pd.read_csv("D:\\IITC\\Study\\Spring 2017\\CS 522\\Project\\GetOldTweets-python-master\\CleanData\\all_data\\alldata.csv")
df = pd.read_csv("D:\\IITC\\Study\\Spring 2017\\CS 522\\Project\\Cleanned_Data.csv", sep=";")


# print df.columns
df = df[df['cleaned_tweet'] != ""]
df_filter = df[df['vader_sentiment'] == df['textblob_sentiment']]
df_neg = df_filter[df_filter['vader_sentiment'] == 'Negative'].head(1100)
df_pos = df_filter[df_filter['vader_sentiment'] == 'Positive'].head(1100)
df_neu = df_filter[df_filter['vader_sentiment'] == 'Neutral'].head(1100)
df_concat = pd.concat([df_neg,df_pos,df_neu],axis=0)
# print len(df_concat)
df_concat = df_concat.sample(frac=1)
df_classifier = df_concat[['cleaned_tweet','vader_sentiment']]
# df_classifier["Cleaned_Tweet"] =  df.Text.str.replace('[^\x00-\x7F]','')
# print df["Text"]

train_split =0.7
import string
from nltk.corpus import stopwords
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation 
print "-------------LogisticRegression--------------"
text_clf = Pipeline([('tfidf', TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words=stop,max_features=10)),('clf', linear_model.LogisticRegression()) ])
text_clf = text_clf.fit(df_classifier['cleaned_tweet'][:int(len(df_classifier)*train_split)], df_classifier['vader_sentiment'][:int(len(df_classifier)*train_split)])
predicted = text_clf.predict(df_classifier['cleaned_tweet'][int(len(df_classifier)*train_split)+1:])
print metrics.classification_report(df_classifier['vader_sentiment'][int(len(df_classifier)*train_split)+1:], predicted)
print "Confusion Matrix"
print metrics.confusion_matrix(df_classifier['vader_sentiment'][int(len(df_classifier)*train_split)+1:], predicted)
print "Accuracy = ",metrics.accuracy_score(df_classifier['vader_sentiment'][int(len(df_classifier)*train_split)+1:], predicted)
print metrics.precision_score(df_classifier['Sentiment'][int(len(df_classifier)*train_split)+1:], predicted)
print metrics.recall_score(df_classifier['Sentiment'][int(len(df_classifier)*train_split)+1:], predicted, average = 'weighted')



print "----------MultinomialNB----------"
text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB(alpha =0,fit_prior=True, class_prior=None))])
text_clf = text_clf.fit(df_classifier['Cleaned_Tweet'][:int(len(df_classifier)*train_split)], df_classifier['Sentiment'][:int(len(df_classifier)*train_split)])
predicted = text_clf.predict(df_classifier['Cleaned_Tweet'][int(len(df_classifier)*train_split)+1:])
print metrics.classification_report(df_classifier['Sentiment'][int(len(df_classifier)*train_split)+1:], predicted)
print "Confusion Matrix"
print metrics.confusion_matrix(df_classifier['Sentiment'][int(len(df_classifier)*train_split)+1:], predicted)
print "Accuracy = ",metrics.accuracy_score(df_classifier['Sentiment'][int(len(df_classifier)*train_split)+1:], predicted)
print metrics.precision_score(df['Tag'][int(len(df)*train_split)+1:], predicted,average = 'weighted')
print metrics.recall_score(df['Tag'][int(len(df)*train_split)+1:], predicted,average = 'weighted')

#checking pipeline parameters
tfidf = text_clf.named_steps['tfidf']
print tfidf
print tfidf.get_feature_names()
idf = tfidf.idf_
print dict(zip(tfidf.get_feature_names(), idf))
countvec = text_clf.named_steps['vect']
print vect


print "-----------SGDClassifier----------"
text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),
	('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, n_iter=5, random_state=42)) ])
text_clf = text_clf.fit(df['Text'][:int(len(df)*train_split)], df['Tag'][:int(len(df)*train_split)])
predicted = text_clf.predict(df['Text'][int(len(df)*train_split)+1:])
# print metrics.classification_report(df['Tag'][int(len(df)*train_split)+1:], predicted)
# print "Confusion Matrix"
# print metrics.confusion_matrix(df['Tag'][int(len(df)*train_split)+1:], predicted)
print metrics.accuracy_score(df['Tag'][int(len(df)*train_split)+1:], predicted)
print metrics.precision_score(df['Tag'][int(len(df)*train_split)+1:], predicted,average = 'weighted')
print metrics.recall_score(df['Tag'][int(len(df)*train_split)+1:], predicted,average = 'weighted')

print "----------LinearSVC-------------"
text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', svm.LinearSVC()) ])
text_clf = text_clf.fit(df_classifier['Cleaned_Tweet'][:int(len(df_classifier)*train_split)], df_classifier['Sentiment'][:int(len(df_classifier)*train_split)])
predicted = text_clf.predict(df_classifier['Cleaned_Tweet'][int(len(df_classifier)*train_split)+1:])

print metrics.classification_report(df_classifier['Sentiment'][int(len(df_classifier)*train_split)+1:], predicted)
print "Confusion Matrix"
print metrics.confusion_matrix(df_classifier['Sentiment'][int(len(df_classifier)*train_split)+1:], predicted)
print "Accuracy = ",metrics.accuracy_score(df_classifier['Sentiment'][int(len(df_classifier)*train_split)+1:], predicted)
print metrics.precision_score(df['Tag'][int(len(df)*train_split)+1:], predicted,average = 'weighted')
print metrics.recall_score(df['Tag'][int(len(df)*train_split)+1:], predicted,average = None)


print "-------------LogisticRegression--------------"
text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', linear_model.LogisticRegression(C=1.0)) ])
text_clf = text_clf.fit(df['Text'][:int(len(df)*train_split)], df['Tag'][:int(len(df)*train_split)])
predicted = text_clf.predict(df['Text'][int(len(df)*train_split)+1:])
print metrics.classification_report(df['Tag'][int(len(df)*train_split)+1:], predicted)
print "Confusion Matrix"
print metrics.confusion_matrix(df['Tag'][int(len(df)*train_split)+1:], predicted)
print metrics.accuracy_score(df['Tag'][int(len(df)*train_split)+1:], predicted)
print metrics.precision_score(df['Tag'][int(len(df)*train_split)+1:], predicted,average = 'weighted')
print metrics.recall_score(df['Tag'][int(len(df)*train_split)+1:], predicted,average = 'weighted')



print "--------PassiveAggressiveClassifier----------"
text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', linear_model.PassiveAggressiveClassifier()) ])
text_clf = text_clf.fit(df['Text'][:int(len(df)*train_split)], df['Tag'][:int(len(df)*train_split)])
predicted = text_clf.predict(df['Text'][int(len(df)*train_split)+1:])
# print metrics.classification_report(df['Tag'][int(len(df)*train_split)+1:], predicted)
# print "Confusion Matrix"
# print metrics.confusion_matrix(df['Tag'][int(len(df)*train_split)+1:], predicted)

print metrics.accuracy_score(df['Tag'][int(len(df)*train_split)+1:], predicted)
print metrics.precision_score(df['Tag'][int(len(df)*train_split)+1:], predicted,average = 'weighted')
print metrics.recall_score(df['Tag'][int(len(df)*train_split)+1:], predicted,average = 'weighted')


conf_matrix=pd.crosstab(df['Tag'], df['Polarity'],margins=True)
print(conf_matrix)
df1 = pd.read_csv("Data_All.csv")
x_pred=pd.Series(df1['Tag'],name='Predicted')
x_act=pd.Series(df1['Sentiment'],name='Actual')
conf_matrix=pd.crosstab(x_act, x_pred,margins=True)
print(conf_matrix)