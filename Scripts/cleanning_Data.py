# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn import linear_model, datasets
from sklearn import metrics
from sklearn.linear_model import SGDClassifier
import pandas as pd,re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from nltk import word_tokenize
from nltk.corpus import stopwords
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.cluster import KMeansClusterer, euclidean_distance


def cleaning_tweets(sentence):
	analyzer = SentimentIntensityAnalyzer()
	pricewords = ["price","amount","bill","cost","demand","discount","estimate","expenditure","expense","fare","fee","figure","output","pay","payment","premium","rate","return","tariff","valuation","worth","appraisal","assessment","barter","bounty","ceiling","charge","compensation","consideration","damage","disbursement","dues","exaction","hire","outlay","prize","quotation","ransom","reckoning","retail","reward","score","sticker","tab","ticket","toll","tune","wages","wholesale","appraisement","asking price","face value"]
	servicewords =["account","assistance","benefit","business","duty","employment","maintenance","office","supply","use","utility","work","advantage","applicability","appropriateness","avail","check","courtesy","dispensation","employ","favor","fitness","indulgence","kindness","labor","ministration","overhaul","relevance","serviceability","servicing","usefulness","value"]
	qualitywords = ["quality","aspect","character","condition","element","kind","nature","trait","affection","affirmation","attribute","constitution","description","endowment","essence","factor","genius","individuality","make","mark","parameter","peculiarity","predication","property","savor","sort","virtue","name of tune","nature of beast","way of it"]
	sad_emoticons = {":-(", ":(", ":-|", ";-(", ";-<", "|-{"}
	happy_emoticons = {":-)", ":)", ":o)", ":-}", ";-}", ":->", ";-)"}
	try:
		if TextBlob(sentence).detect_language() == 'en':
			words = set(sentence.split())
			if sad_emoticons & words:
				found_emoji = sad_emoticons & words
				for x in found_emoji:
					sentence.replace(x,"sad")
			if happy_emoticons & words:
				found_emoji=happy_emoticons & words
				for x in found_emoji:
					sentence.replace(x,"happy")
			cleaned_tweet = re.sub(r'(?i)\b((?:https?://*|www*\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', sentence)
			cleaned_tweet = re.sub(r'''(?i)\b((?:http?://*|www*\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))'''
,'',sentence)
			cleaned_tweet = cleaned_tweet.replace("http://","")
			cleaned_tweet = cleaned_tweet.replace("https://","")

			cleaned_tweet = re.sub(r'[#,@]\S*',"",cleaned_tweet)
			vs = analyzer.polarity_scores(cleaned_tweet)
			stop = stopwords.words('english') + list(string.punctuation)
			cleaned_tweet = ' '.join([i for i in cleaned_tweet.lower().split() if i not in stop])
			textblob_polarity = TextBlob(cleaned_tweet.encode("utf-8")).sentiment.polarity

			if textblob_polarity > 0:
				textblob_sentiment = 'Positive'
			elif textblob_polarity < 0:
				textblob_sentiment = 'Negative'
			elif textblob_polarity == 0:
				textblob_sentiment = 'Neutral'
			if vs['compound'] > 0.5:
				vs_sentiment = 'Positive'
			elif vs['compound'] < -0.5:
				vs_sentiment = 'Negative'
			else :
				vs_sentiment = 'Neutral'
			price =0
			service =0
			quality =0
			if len(list(set(sentence.lower().split()) & set(pricewords))) > 0:
				price = 1
			
			if len(list(set(sentence.lower().split()) & set(servicewords))) > 0:
				service = 1
			
			if len(list(set(sentence.lower().split()) & set(qualitywords))) > 0:
				quality = 1
			
			return ["".join(l for l in cleaned_tweet if l not in string.punctuation),vs_sentiment ,vs['compound'] ,textblob_sentiment,textblob_polarity,price,service,quality]
	except Exception, e:
		return None

df = pd.read_csv("D:\\IITC\\Study\\Spring 2017\\CS 522\\Project\\GetOldTweets-python-master\\RawData\\all_data\\all_rawdata_city.csv")
df['cleaned_tweet']=0
df['vader_sentiment']=0
df['vader_score']=0
df['textblob_sentiment']=0
df['textblob_score']=0
df['price']=0
df['service']=0
df['quality']=0
count=0
for index, row in df.iterrows():
	sentence=row['Text']
	processed = cleaning_tweets(sentence)
	print count , index

	try:
		df['cleaned_tweet'][index]=processed[0]
		df['vader_sentiment'][index]=processed[1]
		df['vader_score'][index]=processed[2]
		df['textblob_sentiment'][index]=processed[3]
		df['textblob_score'][index]=processed[4]
		df['price'][index]=processed[5]
		df['service'][index]=processed[6]
		df['quality'][index]=processed[7]
		count +=1
	except Exception, e:
		pass
	
df =df[df['vader_sentiment']!=0]
df.to_csv("Cleanned_Data.csv",sep=";")