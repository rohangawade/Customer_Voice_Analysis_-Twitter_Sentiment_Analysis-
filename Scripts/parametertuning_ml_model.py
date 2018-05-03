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
import matplotlib.pyplot as plt 
from sklearn.model_selection import cross_val_score

df = pd.read_csv("D:\\IITC\\Study\\Spring 2017\\CS 522\\Project\\GetOldTweets-python-master\\CleanData\\all_data\\alldata.csv")

df_filter = df[df['Sentiment'] == df['Lexicon_polarity']]
df_neg = df_filter[df_filter['Lexicon_polarity'] == 'Negative'].head(1100)
df_pos = df_filter[df_filter['Lexicon_polarity'] == 'Positive'].head(1100)
df_neu = df_filter[df_filter['Lexicon_polarity'] == 'Neutral'].head(1100)

df_concat = pd.concat([df_neg,df_pos,df_neu],axis=0)
# print len(df_concat)

df_concat = df_concat.sample(frac=1)
df_classifier = df_concat[['Cleaned_Tweet','Sentiment']]
# df_classifier["Cleaned_Tweet"] =  df.Text.str.replace('[^\x00-\x7F]','')
# print df["Text"]

train_split =0.7

# print "----------LinearSVC-------------"
text_clf = Pipeline([('tfidf', TfidfVectorizer()),('clf', svm.LinearSVC())])
text_clf = text_clf.fit(df_classifier['Cleaned_Tweet'][:int(len(df_classifier)*train_split)], df_classifier['Sentiment'][:int(len(df_classifier)*train_split)])
predicted = text_clf.predict(df_classifier['Cleaned_Tweet'][int(len(df_classifier)*train_split)+1:])
print cross_val_score(text_clf, df_classifier['Cleaned_Tweet'], df_classifier['Sentiment'], groups=None, scoring='accuracy', cv=10, n_jobs=1, verbose=0, fit_params=None, pre_dispatch='2*n_jobs')
print metrics.classification_report(df_classifier['Sentiment'][int(len(df_classifier)*train_split)+1:], predicted)
print "Confusion Matrix"
print metrics.confusion_matrix(df_classifier['Sentiment'][int(len(df_classifier)*train_split)+1:], predicted)
print "Accuracy = ",metrics.accuracy_score(df_classifier['Sentiment'][int(len(df_classifier)*train_split)+1:], predicted)

print metrics.precision_score(df['Tag'][int(len(df)*train_split)+1:], predicted,average = 'weighted')
print metrics.recall_score(df['Tag'][int(len(df)*train_split)+1:], predicted,average = None)
accuracy_list=[]
for c in range(1,40):
	text_clf = Pipeline([('tfidf', TfidfVectorizer()),('clf', svm.LinearSVC(penalty='l2', loss='hinge', dual=True, tol=0.0001, C=c, multi_class='ovr', fit_intercept=True, intercept_scaling=1, class_weight=None, verbose=0, random_state=None, max_iter=1000))])
	text_clf = text_clf.fit(df_classifier['Cleaned_Tweet'][:int(len(df_classifier)*train_split)], df_classifier['Sentiment'][:int(len(df_classifier)*train_split)])
	predicted = text_clf.predict(df_classifier['Cleaned_Tweet'][int(len(df_classifier)*train_split)+1:])
	print c
	accuracy_list.append({'param':c*c,'accuarcy':metrics.accuracy_score(df_classifier['Sentiment'][int(len(df_classifier)*train_split)+1:], predicted)})
	print metrics.classification_report(df_classifier['Sentiment'][int(len(df_classifier)*train_split)+1:], predicted)
	print "Confusion Matrix"
	print metrics.confusion_matrix(df_classifier['Sentiment'][int(len(df_classifier)*train_split)+1:], predicted)
	print "Accuracy = ",metrics.accuracy_score(df_classifier['Sentiment'][int(len(df_classifier)*train_split)+1:], predicted)

print accuracy_list
df_list = pd.DataFrame(accuracy_list)
# print df_list.head()


plt.plot(df_list['param'], df_list['accuarcy'])
plt.xlabel("Change in regularization value")
plt.ylabel("Accuracy")

plt.show()