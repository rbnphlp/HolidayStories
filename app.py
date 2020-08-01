
from flask import Flask,render_template,request,redirect,url_for
from flask_pymongo import PyMongo 
import requests
from bson.objectid import ObjectId
import os 
from dotenv import load_dotenv


"Load enviornment variables"
load_dotenv()

MONGO_URI=os.getenv("MONGO_URI")

"Configure flask app "

app=Flask(__name__)

app.config['MONGO_DBNAME']="HolidayStories"
app.config["MONGO_URI"]=MONGO_URI

mongo=PyMongo(app)



@app.route('/')
def index():
    return ("Hello world! Test to deploy on heroku"+MONGO_URI)



"Read Holiday Pages"

@app.route("/add_holidays")
def added_holidays():

    return(render_template("holidays.html",holidays=mongo.db.Holidays.find()))

if __name__=="__main__":
        app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)