
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


@app.route('/get_holidays',methods=["GET","POST"])
def get_holidays():
    
    Holidays = mongo.db.Holidays.find()
    return(render_template("Add_Holiday.html",holidays=Holidays))


"Read Holiday Pages for Holiday only Pages"

@app.route("/add_holidays",methods=["GET","POST"])
def added_holidays():

    return(render_template("holidays.html",holidays=mongo.db.Holidays.find()))


"Read Holidays and correponding memories"

@app.route('/added_holiday_memories')
def added_holiday_memories():
   
    "Do a join/lookup to get memories of the holiday specified :"

    holiday_memories=mongo.db.Holidays.aggregate([{"$lookup": 
                    {
    "from": 'Memories',
    "localField": '_id',
    "foreignField": 'Holidays_id',
    "as": 'Holiday_Memories'
                    }} ,

    {"$unwind":"$Holiday_Memories"}
    ])

    return(render_template("Added_memories.html",memories=holiday_memories))


"Add Holidays Page"

@app.route("/Add_Holidays",methods=["GET","POST"])
def Add_Holidays():
    

    Holidays = mongo.db.Holidays
    Holidays.insert_one(request.form.to_dict())
    

    return(redirect(url_for("get_holidays")))




"Delete Holidays in Holidays Page"


@app.route("/delete_holiday/<Holidays_id>")
def delete_holiday(Holidays_id):
    mongo.db.Holidays.remove({"_id": ObjectId(Holidays_id)})


    return(redirect(url_for("get_holidays")))

    





if __name__=="__main__":
        app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)