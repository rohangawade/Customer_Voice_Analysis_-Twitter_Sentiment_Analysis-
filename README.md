# Customer_Voice_Analysis_-Twitter_Sentiment_Analysis-
CS 522- Advanced Data Mining Project.
<li>Crawled Twitter data across various brands in different categories (Food, Retail, and Clothing).
<li>Cleaned the tweets using Natural Language Processing steps to clean the data. Found most common words.
<li>Label tweets using vader sentiment and Textblob.
<li>Created different machine learning models pipeline using Logistic Regression, Multinomial Naive Bayes, Support Vector Machine, Stocastic
Gradient Descent, Passive Aggressive Classifier to predict the sentiments.
<li>Created a Data Visualization dashboard to display how the brand is performing with respect to popularity, positive and negative sentiments across different citites in US. Hosted on AWS.
<li> Technology:  Python, scikitlearn, nltk, NLP, flask, html5, bootstrap, Twitter Stream/Search API, AWS EC2, Amazon Cloud.
  
 <b>Result</b>
 <li>Dashboard <br>
  The dashboard displays tweets across one month timespan. People tweeted more about McDonalds at the start of April. Also the number of price and service mentioned tweets are displayed at the right hand side. 
  <img src="images/dashboard.png" />
<li> Detailed report for Chicago area<br>
 Analysis
McDonalds is popular in Chicago, burgerking is having more percentage of people tweeting positive tweets and papajohns has more percentage of people tweeting negative tweets.
  <img src="/images/Food_Chicago.JPG" />
  <li> Price and Service Related Analysis
   Analysis
• From the above plots we can see that McDonalds has the maximum number of positive and negative tweets with respect to price and service related words.
• Pizza hut seems to be costly as the number of negative tweets related to price words are more than positive tweets. Same is for burgerking, dominos and papajohns(Price Mentions Graph)
• Service related words have more number of positive tweets for burgerking, dominos mcdonalds and pizzahut. But papajohns service seems to be having more negative tweets. (Service Mentions Graph)
    <img src="/images/PriceServiceMentioned.JPG" />
    
