# -*- coding: utf-8 -*-
import preprocessor as p
import nltk
import urllib,urllib2,json,re,datetime,sys,cookielib
from pyquery import PyQuery
import sys,getopt,datetime,codecs
from textblob import TextBlob

p.set_options(p.OPT.URL, p.OPT.EMOJI)

price =[]
quality = []
service = []

def cleanningtweet(tweet):
	tweet =tweet
	words = nltk.word_tokenize(tweet)
	words=[word.lower() for word in words if word.isalpha()]
	tweet = ' '.join(words)
	return tweet

def sentiment_val(cleantweet):
	text = TextBlob(cleantweet)
	sentiment_score = text.sentiment.polarity
	if sentiment_score > 0.00:
		sentiment = "Positive"
	elif sentiment_score < 0:
		sentiment = "Negative"
	else:
		sentiment = "Neutral"

	return sentiment_score,sentiment

def categorty(tweet):
	return [1,0,1]

	
	
class Tweet:
	def __init__(self):
		pass
		
		
class TweetCriteria:
	
	def __init__(self):
		self.maxTweets = 0
		
	def setUsername(self, username):
		self.username = username
		return self
		
	def setSince(self, since):
		self.since = since
		return self
	
	def setUntil(self, until):
		self.until = until
		return self
		
	def setQuerySearch(self, querySearch):
		self.querySearch = querySearch
		return self

	def setNear(self, near):
		self.near = near
		return self
	def setWithin(self, within):
		self.within = within
		return self	

	def setMaxTweets(self, maxTweets):
		self.maxTweets = maxTweets
		return self

	def setTopTweets(self, topTweets):
		self.topTweets = topTweets
		return self


class TweetManager:
	
	def __init__(self):
		pass
		
	@staticmethod
	def getTweets(tweetCriteria, receiveBuffer = None, bufferLength = 100):
		refreshCursor = ''
	
		results = []
		resultsAux = []
		cookieJar = cookielib.CookieJar()
		
		if hasattr(tweetCriteria, 'username') and (tweetCriteria.username.startswith("\'") or tweetCriteria.username.startswith("\"")) and (tweetCriteria.username.endswith("\'") or tweetCriteria.username.endswith("\"")):
			tweetCriteria.username = tweetCriteria.username[1:-1]

		active = True

		while active:
			json = TweetManager.getJsonReponse(tweetCriteria, refreshCursor, cookieJar)
			if len(json['items_html'].strip()) == 0:
				break

			refreshCursor = json['min_position']			
			tweets = PyQuery(json['items_html'])('div.js-stream-tweet')
			
			if len(tweets) == 0:
				break
			 
			for tweetHTML in tweets:
				tweetPQ = PyQuery(tweetHTML)
				tweet = Tweet()
				
				usernameTweet = tweetPQ("span.username.js-action-profile-name b").text();
				txt = re.sub(r"\s+", " ", tweetPQ("p.js-tweet-text").text().replace('# ', '#').replace('@ ', '@'));
				retweets = int(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""));
				favorites = int(tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""));
				dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"));
				id = tweetPQ.attr("data-tweet-id");
				permalink = tweetPQ.attr("data-permalink-path");
				
				geo = ''
				geoSpan = tweetPQ('span.Tweet-geo')
				if len(geoSpan) > 0:
					geo = geoSpan.attr('title')
				
				tweet.id = id
				tweet.permalink = 'https://twitter.com' + permalink
				tweet.username = usernameTweet
				tweet.text = txt
				tweet.date = datetime.datetime.fromtimestamp(dateSec)
				tweet.retweets = retweets
				tweet.favorites = favorites
				tweet.mentions = " ".join(re.compile('(@\\w*)').findall(tweet.text))
				tweet.hashtags = " ".join(re.compile('(#\\w*)').findall(tweet.text))
				tweet.geo = geo
				
				results.append(tweet)
				resultsAux.append(tweet)
				
				if receiveBuffer and len(resultsAux) >= bufferLength:
					receiveBuffer(resultsAux)
					resultsAux = []
				
				if tweetCriteria.maxTweets > 0 and len(results) >= tweetCriteria.maxTweets:
					active = False
					break
					
		
		if receiveBuffer and len(resultsAux) > 0:
			receiveBuffer(resultsAux)
		
		return results
	
@staticmethod
def getJsonReponse(tweetCriteria, refreshCursor, cookieJar):

		url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&max_position=%s"
		urlGetData = ''
		
		
		if hasattr(tweetCriteria, 'username'):
			urlGetData += ' from:' + tweetCriteria.username
			
		if hasattr(tweetCriteria, 'since'):
			urlGetData += ' since:' + tweetCriteria.since
			
		if hasattr(tweetCriteria, 'until'):
			urlGetData += ' until:' + tweetCriteria.until
			
		if hasattr(tweetCriteria, 'querySearch'):
			urlGetData += ' ' + tweetCriteria.querySearch

		if hasattr(tweetCriteria, 'near'):
			urlGetData += ' near:' + tweetCriteria.near
		
		if hasattr(tweetCriteria, 'within'):
			urlGetData += ' within:' + tweetCriteria.within
			
		if hasattr(tweetCriteria, 'topTweets'):
			if tweetCriteria.topTweets:
				url = "https://twitter.com/i/search/timeline?q=%s&src=typd&max_position=%s"

		url = url % (urllib.quote(urlGetData), refreshCursor)

		headers = [
			('Host', "twitter.com"),
			('User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"),
			('Accept', "application/json, text/javascript, */*; q=0.01"),
			('Accept-Language', "de,en-US;q=0.7,en;q=0.3"),
			('X-Requested-With', "XMLHttpRequest"),
			('Referer', url),
			('Connection', "keep-alive")
		]

		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
		opener.addheaders = headers

		try:
			response = opener.open(url)
			jsonResponse = response.read()
		except:
			print "Twitter weird response. Try to see on browser: https://twitter.com/search?q=%s&src=typd" % urllib.quote(urlGetData)
			sys.exit()
			return
		
		dataJson = json.loads(jsonResponse)
	
	return dataJson

def main(argv)

	if len(argv) == 0:
		print 'You must pass some parameters. Use \"-h\" to help.'
		return
		
	if len(argv) == 1 and argv[0] == '-h':
		print """\nTo use this jar, you can pass the folowing attributes:
		username: Username of a specific twitter account (without @)
		since: The lower bound date (yyyy-mm-aa)
		until: The upper bound date (yyyy-mm-aa)
		querysearch: A query text to be matched
		maxtweets: The maximum number of tweets to retrieve

		\nExamples:
		# Example 1 - Get tweets by username [barackobama]
		python Exporter.py --username "barackobama" --maxtweets 1\n

		# Example 2 - Get tweets by query search [europe refugees]
		python Exporter.py --querysearch "europe refugees" --maxtweets 1\n

		# Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']
		python Exporter.py --username "barackobama" --since 2015-09-10 --until 2015-09-12 --maxtweets 1\n
 
		# Example 4 - Get the last 10 top tweets by username
		python Exporter.py --username "barackobama" --maxtweets 10 --toptweets\n"""
		return
 
	try:
		opts, args = getopt.getopt(argv, "", ("username=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=","near=","within="))
		
		tweetCriteria = TweetCriteria()
		
		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg
				
			elif opt == '--since':
				tweetCriteria.since = arg
				
			elif opt == '--until':
				tweetCriteria.until = arg
				
			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg
				brand =arg
			elif opt == '--toptweets':
				tweetCriteria.topTweets = True
				
			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)

			elif opt == '--near':
				tweetCriteria.near = arg
				location =arg
			elif opt == '--within':
				tweetCriteria.within = arg
				
		filename = "output_"+brand+"_"+location+".csv"
		print filename
		outputFile = codecs.open(filename, "w+", "utf-8")
		
		# outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')
		
		print 'Searching...\n'
		
		def receiveBuffer(tweets):
			for t in tweets:
				sentiment_score,sentiment = sentiment_val(cleanningtweet(t.text))
				# outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s;%0.3f,%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, tweetCriteria.near, t.mentions, t.hashtags, t.id, t.permalink,sentiment_score,sentiment)))
				outputFile.write(('\n%s;%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s;%0.3f;%s' % (brand,'Food',t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, tweetCriteria.near, t.mentions, t.hashtags, t.id, t.permalink,sentiment_score,sentiment)))
			outputFile.flush();
			print 'More %d saved on file...\n' % len(tweets)
		
		TweetManager.getTweets(tweetCriteria, receiveBuffer)
		
	except arg:
		print 'Arguments parser error, try -h' + arg
	finally:
		outputFile.close()
		print 'Done. Output file generated "output_got.csv".'

if __name__ == '__main__':
	main(sys.argv[1:])