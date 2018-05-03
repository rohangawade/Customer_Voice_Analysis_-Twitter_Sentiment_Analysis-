from datetime import datetime
import pandas as pd
from pymongo import MongoClient
data=[]
clinet = MongoClient('127.0.0.1',27017)
conn=clinet["ADM"]["dummy3"]
brands =conn.find().distinct("Category")
location = conn.find().distinct("Geo")
categoryquery=brands[0]
locationed=location[0]
for x in conn.find({"Category":brands[0],"Geo":location[0]}):
    data.append(x)
    print x
clinet.close()
