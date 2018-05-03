# -*- coding: utf-8 -*-
from nltk.tokenize import word_tokenize
import nltk
import preprocessor as p
p.set_options(p.OPT.URL, p.OPT.EMOJI)

 # nltk.download('all')
 # tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
# print(word_tokenize(tweet))

import re
# regex_str = [ r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
#    r"(?:[a-z][a-z'\-_]+[a-z])" # words with - and '
#              ]

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]


tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(str(s))
 
def preprocess(s, lowercase=False):
    # s = s.decode('unicode_escape').encode('ascii','ignore')
    print s
    s = re.sub(r"http\S+.*", "", s)
    s = p.clean(s)
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        # tokens = [token.lower() for token in tokens]
    return tokens

# tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
import pandas as pd
from collections import Counter
# fname = 'mytweets.json'
count_all = Counter()
# df = pd.read_csv('D:\\IITC\\Study\\Spring 2017\\CS 522\\Project\\GetOldTweets-python-master\\output_got.csv')
df = pd.read_csv('Cleanned_Data.csv',sep=';')

#stopwords
from nltk.corpus import stopwords
import string
 
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation 
df["Text"] =  df.Text.str.replace('[^\x00-\x7F]','')
for tweet in df['Text']:
    try:
        # print df['Text']

        # terms_all = [term for term in preprocess(tweet)]
        # print terms_all
        terms_stop = [term for term in preprocess(tweet) if term not in stop]
        # print(terms_stop)
        sent = ' '.join(terms_stop)

        print sent
        # count_all.update(terms_all)
        count_all.update(terms_stop)

    except Exception, e:
        raise
    finally:
        pass


mostcommon_words = count_all.most_common()

import pandas as pd
df_mostcommon =pd.DataFrame(mostcommon_words)
df_mostcommon.to_csv('MostCommon.csv', index=False, header=False)

from nltk import bigrams 
terms_bigram = bigrams(terms_stop)
df_mostcommon_biggram =pd.DataFrame(terms_bigram)
df_mostcommon_biggram.to_csv('MostCommon_BigGram_Dominos.csv', index=False, header=False)
