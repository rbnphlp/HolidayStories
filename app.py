
from flask import Flask,render_template,request,redirect,url_for
from flask_pymongo import PyMongo 
import requests
from bson.objectid import ObjectId
import os 
from dotenv import load_dotenv
import ast
import boto3


"Load enviornment variables"
load_dotenv()

MONGO_URI=os.getenv("MONGO_URI")


S3_bucket=os.getenv("S3_bucket")
S_Key=os.getenv("S_KEY")
AC_KEY=os.getenv("AC_KEY")


"Configure flask app "

app=Flask(__name__)

app.config['MONGO_DBNAME']="HolidayStories"
app.config["MONGO_URI"]=MONGO_URI

mongo=PyMongo(app)



"Set up S3"

S3_bucket=os.getenv("S3_bucket")
S_Key=os.getenv("S_KEY")
AC_KEY=os.getenv("AC_KEY")


s3 = boto3.resource('s3',
        aws_access_key_id=AC_KEY,
        aws_secret_access_key= S_Key)


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

    

" Send Holidays Id   into Memories Page"
@app.route("/Add_memories/<Holidays_id>")
def Add_memories(Holidays_id):

    
    Holiday=mongo.db.Holidays.find_one({"_id": ObjectId(Holidays_id)})

 
    return(render_template('Add_memories.html',Holiday=Holiday))



" Submit memory info to mongodb & AWS  including HolidayID + imagelink "  

@app.route("/Submit_Memory/<Holidays_id>",methods=["GET","POST"])
def Submit_Memory(Holidays_id):
    print("Hello")
    print("Holidays passed: "+ Holidays_id)
    print("form"+str(request.form.to_dict()))
    Memories_db=mongo.db.Memories

    Memories_db.insert(request.form.to_dict())


    return(render_template('Add_memories.html',Holiday=Holidays_id))



@app.route("/get_aws_files")
def get_aws_files():
    my_bucket=s3.Bucket(S3_bucket)
    summaries=my_bucket.objects.all()
    
    print("my bucket"+str(my_bucket))
    
    

    return(render_template("aws_files.html",my_bucket=my_bucket,files=summaries))


if __name__=="__main__":
        app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)