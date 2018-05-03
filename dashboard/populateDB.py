#!/usr/bin/python

from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def main():
    # Connect to the DB
    collection = MongoClient('127.0.0.1',27017)["ADM"]["users"]

    # Ask for data to store
    user = "demo"
    password = "demo"
    role="manager"
    
    name="TeamADM_new"
    email="abhishekbhardwaj13506@gmail.com"
    validity="01/12/2017"
    active="true"

    pass_hash = generate_password_hash(password, method='pbkdf2:sha256')
    phone=""
    try:
        collection.insert({"_id": user, "password": pass_hash,"role":role,"name":name,"email":email,"validity":validity,"status":active,'phone':phone})
        print "User created."
    except DuplicateKeyError:
        print "User already present in DB."


if __name__ == '__main__':
    main()
