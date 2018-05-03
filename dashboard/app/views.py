from app import app, lm
from flask import request, redirect, render_template, url_for, flash,session,make_response,jsonify
from flask.ext.login import login_user, logout_user, login_required
from .forms import LoginForm
from flask import send_from_directory
from pymongo import MongoClient


import flask,ast
from .user import User
from datetime import datetime
import numpy as np
import json,time,io
from collections import defaultdict
import os, sys,csv
from pymongo import MongoClient
from bson import json_util
import redis
import subprocess
from werkzeug import secure_filename

import numpy as np
import requests ,re ,csv,string
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
import pandas as pd
from nltk import pos_tag
import time
imageratio = str(0.9)
descriptionration= str(0.1)
result=[]
app.config['UPLOAD_FOLDER'] = 'app/static/img/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation


# Route that will process the file upload
@app.route('/upload',methods=['POST'])
def upload():
    print request.form  
    data=[]
    categoryquery=request.form['category']
    locationed=request.form['location']
    print categoryquery,locationed
    clinet = MongoClient('127.0.0.1',27017)
    conn=clinet["ADM"]["dummy4"]
    brands =conn.find().distinct("Category")
    location = conn.find().distinct("Geo")
    location.append("All")

    if locationed =="All":
        T = conn.find({"Category":categoryquery})
    else:
        T = conn.find({"Category":categoryquery,"Geo":locationed})
    leg=['Date']
    colname =[]
    for x in T:
        data.append(x)
    clinet.close()
    df_all =pd.DataFrame(data)
    #df_all['Date']=df_all['Date'].apply(lambda x: datetime.strptime(x,"%m/%d/%Y").strftime('%m/%d/%Y'))
    #df_all['Date'] = df_all['Date'].apply(lambda x: datetime.strptime(x,"%m/%d/%Y %H:%M"))
    #df_all['Date'] = df_all['Date'].apply(lambda x: datetime.strptime(x,"%m/%d/%y"))
    df_all['Date'] = df_all['Date'].apply(lambda x: datetime.strptime(x,"%m/%d/%Y"))
    cards_result=[]
    graph =[]

    for x  in df_all.Brand.unique():
        df = df_all[df_all['Brand']==x]
	df['predicted_sentiment']=df['vader_sentiment']
        pos = len(df[df['predicted_sentiment']=="Positive"])
        neg = len(df[df['predicted_sentiment']=="Negative"])
        neu = len(df[df['predicted_sentiment']=="Neutral"])
        price_pos =sum(df[df['predicted_sentiment']=="Positive"]['price'])
        price_neg =sum(df[df['predicted_sentiment']=="Negative"]['price'])
        price_neu =sum(df[df['predicted_sentiment']=="Negative"]['price'])
        qualtiy_pos =sum(df[df['predicted_sentiment']=="Positive"]['quality'])
        qualtiy_neg =sum(df[df['predicted_sentiment']=="Negative"]['quality'])
        qualtiy_neu =sum(df[df['predicted_sentiment']=="Negative"]['quality'])
        service_pos =sum(df[df['predicted_sentiment']=="Positive"]['service'])
        service_neg =sum(df[df['predicted_sentiment']=="Negative"]['service'])
        service_neu =sum(df[df['predicted_sentiment']=="Negative"]['service'])
        cards_result.append({"total":len(df_all),"brand":x,"pos":pos,"neg":neg,"neu":neu,"pp":pos/(pos+neg+neu+1),"price_pos":price_pos,"price_neg":price_neg,"price_neu":price_neu,"quality_pos":qualtiy_pos,"quality_neg":qualtiy_neg,"quality_neu":qualtiy_neu,"service_pos":service_pos,"service_neg":service_neg,"service_neu":service_neu})
        temp = df.set_index('Date').groupby(pd.TimeGrouper('W')).size()
        temp_pos = df[df['predicted_sentiment']=="Positive"].set_index('Date').groupby(pd.TimeGrouper('W')).size()
        temp_neg = df[df['predicted_sentiment']=="Negative"].set_index('Date').groupby(pd.TimeGrouper('W')).size()
        temp_neu = df[df['predicted_sentiment']=="Neutral"].set_index('Date').groupby(pd.TimeGrouper('W')).size()
        temp_pp = temp_pos*100.0/(temp+1)
        graph.append(temp)
        graph.append(temp_pos)
        graph.append(temp_neg)
        graph.append(temp_neu)
        graph.append(temp_pp)
        colname.append(x+"_total")
        colname.append(x+"_pos")
        colname.append(x+"_neg")
        colname.append(x+"_neu")
        colname.append(str(x+"_pp"))
        leg.append(str(x+"_pp"))

    graph = pd.concat(graph, axis=1)
    graph =graph.fillna(0)
    graph.columns =colname
    print graph
    temp =[]
    for index, row in graph.iterrows():
        each_week =[]
        each_week.append( int(index.strftime("%s")))
        for l in leg[1:]:
            each_week.append(row[l])
        temp.append(each_week)

    return render_template('index.html',legends=leg,data=data,category=brands,location=location,temp=temp,locationtag=locationed,serchtag=categoryquery,card=cards_result)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data) and user[u'status']==u'true':
            user_obj = User(user['_id'])
            login_user(user_obj)
	    session['logged_in'] = True
	    session['user'] = user            
	    flash("Logged in successfully!", category='success')
	    if user['role']=='admin':
	    	return render_template('login.html', title='login', form=form)
            else:
            	return redirect(request.args.get("next") or url_for("index"))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)

@app.route('/user',methods=["POST"])
def user():
	user_obj=session.get('user',None)
	user_obj['group']=list(set(user_obj['group']))
	return json.dumps(user_obj)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    logout_user()
    return redirect(url_for('login'))


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    data=[]
    clinet = MongoClient('127.0.0.1',27017)
    conn=clinet["ADM"]["dummy4"]
    brands =conn.find().distinct("Category")
    location = conn.find().distinct("Geo")
    location.append('All')
    categoryquery=brands[0]
    locationed=location[0]
    leg=['Date']
    colname =[]
    for x in conn.find({"Category":brands[0],"Geo":location[0]}):
        data.append(x)
    clinet.close()
    df_all =pd.DataFrame(data)
    #df_all['Date']=df_all['Date'].apply(lambda x: datetime.strptime(x,"%m/%d/%Y %H:%M").strftime('%m/%d/%Y'))
    #df_all['Date'] = df_all['Date'].apply(lambda x: datetime.strptime(x,"%m/%d/%Y %H:%M").strftime('%m/%d/%Y %H:%M'))
    df_all['Date'] = df_all['Date'].apply(lambda x: datetime.strptime(x,"%m/%d/%Y"))
    cards_result=[]
    graph =[]
    
    for x  in df_all.Brand.unique():
        df = df_all[df_all['Brand']==x]
	df['predicted_sentiment']=df['vader_sentiment']
        pos = len(df[df['predicted_sentiment']=="Positive"])
        neg = len(df[df['predicted_sentiment']=="Negative"])
        neu = len(df[df['predicted_sentiment']=="Neutral"])
        price_pos =sum(df[df['predicted_sentiment']=="Positive"]['price'])
        price_neg =sum(df[df['predicted_sentiment']=="Negative"]['price'])
        price_neu =sum(df[df['predicted_sentiment']=="Negative"]['price'])
        qualtiy_pos =sum(df[df['predicted_sentiment']=="Positive"]['quality'])
        qualtiy_neg =sum(df[df['predicted_sentiment']=="Negative"]['quality'])
        qualtiy_neu =sum(df[df['predicted_sentiment']=="Negative"]['quality'])
        service_pos =sum(df[df['predicted_sentiment']=="Positive"]['service'])
        service_neg =sum(df[df['predicted_sentiment']=="Negative"]['service'])
        service_neu =sum(df[df['predicted_sentiment']=="Negative"]['service'])
        cards_result.append({"total":len(df_all),"brand":x,"pos":pos,"neg":neg,"neu":neu,"pp":pos/(pos+neg+neu+1),"price_pos":price_pos,"price_neg":price_neg,"price_neu":price_neu,"quality_pos":qualtiy_pos,"quality_neg":qualtiy_neg,"quality_neu":qualtiy_neu,"service_pos":service_pos,"service_neg":service_neg,"service_neu":service_neu})
        temp = df.set_index('Date').groupby(pd.TimeGrouper('W')).size()
        temp_pos = df[df['predicted_sentiment']=="Positive"].set_index('Date').groupby(pd.TimeGrouper('W')).size()
        temp_neg = df[df['predicted_sentiment']=="Negative"].set_index('Date').groupby(pd.TimeGrouper('W')).size()
        temp_neu = df[df['predicted_sentiment']=="Neutral"].set_index('Date').groupby(pd.TimeGrouper('W')).size()
        temp_pp = temp_pos*100.0/(temp+1)
        graph.append(temp)
        graph.append(temp_pos)
        graph.append(temp_neg)
        graph.append(temp_neu)
        graph.append(temp_pp)
        colname.append(x+"_total")
        colname.append(x+"_pos")
        colname.append(x+"_neg")
        colname.append(x+"_neu")
        colname.append(str(x+"_pp"))
        leg.append(str(x+"_pp"))

    graph = pd.concat(graph, axis=1)
    graph =graph.fillna(0)
    graph.columns =colname
    print graph
    temp =[]
    for index, row in graph.iterrows():
        each_week =[]
        each_week.append( int(index.strftime("%s")))

        for l in leg[1:]:
            each_week.append(row[l])
        temp.append(each_week)

    return render_template('index.html',legends=leg,data=data,category=brands,location=location,temp=temp,locationtag=locationed,serchtag=categoryquery,card=cards_result)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html')


@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])
