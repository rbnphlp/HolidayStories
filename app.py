
from flask import Flask,render_template,request,redirect,url_for
from flask_pymongo import PyMongo 
import requests
from bson import ObjectId,json_util
import os 
from dotenv import load_dotenv
import ast
import boto3

import json

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



client = boto3.client('s3',
                          region_name='eu-west-2',
                          
                          aws_access_key_id=AC_KEY,
                          aws_secret_access_key=S_Key)

s3 = boto3.resource('s3',
        aws_access_key_id=AC_KEY,
        aws_secret_access_key= S_Key)


@app.route('/')
def index():
    return ("Hello world! Test to deploy on heroku"+MONGO_URI)


@app.route('/get_holidays',methods=["GET","POST"])
def get_holidays():
    
    Holidays = mongo.db.Holidays.find()

    " Send a Holidays & Memeorues joined to the template"
      
    holiday_memories=mongo.db.Holidays.aggregate([{"$lookup": 
                    {
    "from": 'Memories',
    "localField": '_id',
    "foreignField": 'Holidays_id',
    "as": 'Holiday_Memories'
                    }} ,

    {"$unwind":"$Holiday_Memories"}
    ])

    Memories=[]
    Memory_ids=[]
    for memory in holiday_memories:
        Memories.append(memory['Holiday_Memories']['Holidays_id'])
        Memories.append(memory['Holiday_Memories']['_id'])
    


    return(render_template("Add_Holiday.html",holidays=Holidays,Memories=Memories,Memories_id=Memory_ids))


@app.route('/get_memories/',methods=["GET","POST"])
def get_memories():
    
    return(render_template("Add_Holiday.html",holidays=mongo.db.Holidays.find()))





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

    " Check if memories is not null then  render with no "
    Memories_check=mongo.db.Memories.find_one({"Holidays_id":ObjectId(Holidays_id)})
    
    Memories=mongo.db.Memories.find({"Holidays_id":ObjectId(Holidays_id)})
    
    
    if Memories_check is None:
        print("No Memory added")
        Memory_to_show= render_template('Add_memories.html',Holiday=Holiday)
    

    else :
        print("Memory already added")
        
        Memory_to_show=render_template('Add_extra_memories.html',Memories=Memories,Holiday=Holiday)

    return(Memory_to_show)



" Submit memory info to mongodb & AWS  including HolidayID + imagelink "  

@app.route("/Submit_Memory/<Holidays_id>",methods=["GET","POST"])
def Submit_Memory(Holidays_id):
    
  

        print("submitting Text infor to mongo")

        print("form info "+ str(request.form))
        "Jsonify data returned from mongodb"
        jsoned_holidays=json.loads(json_util.dumps(Holidays_id))


        print('jsoned_holiday'+jsoned_holidays)
        "Get holiday id "
        Holidays_id_=jsoned_holidays


        " convert id into a dic type and"
        form_dict= request.form.to_dict()


        form_dict["Holidays_id"]=ObjectId(Holidays_id_)
        Memories_db=mongo.db.Memories
        Memory_id=Memories_db.insert(form_dict)


          
        "Add image Path for the Image link"
        if request.files['File_submission'].filename == '':
            print("No file sumbitted ")
        else:

            "get some information for file upload" 
            file=request.files['File_submission']
            content_type = request.mimetype
            S3_bucket=os.getenv("S3_bucket")

           
            " Get Memory Id for the inserted image"
            print("Memory_id"+str(Memory_id))
            memory_img="https://holidaystories.s3.eu-west-2.amazonaws.com/"+file.filename

            "submit Memory_link to mongo"
            print("Inserting Memory Img Link to mong")
            Memories_db.update({"_id":Memory_id},{"$set": {"Memory_uploaded":memory_img}})

            "Submission form for AWS for the image"
           
            
            "give permissions to make file public so readable:"
            client.put_object(Body=file,Bucket=S3_bucket,
                      Key=file.filename,
                      ContentType='image/jpeg',ACL='public-read')

          


        return(redirect(url_for('Add_memories',Holidays_id=Holidays_id)))


"Editt/Update Memories for a given Memory"

@app.route("/delete_memories/<memory_id>")
def delete_memories(memory_id):
    
    "Find Holidayid of the memory id: to pass on  "
    Memories=mongo.db.Memories.find({"_id":ObjectId(memory_id)})
    
    print("getting memories")
    for Memory in Memories:
        Holiday_id=Memory['Holidays_id']
    "Delete the Memory :"

    mongo.db.Memories.remove({"_id": ObjectId(memory_id)})
    
    
    return(redirect(url_for('Add_memories',Holidays_id=Holiday_id)))


@app.route("/edit_memories")
def edit_memories():
    "for a memory id  re- populate the form and and send add_memories"

"For a given Holiday id Get all the memories: "

@app.route("/view_memories")
def view_memories():

    return(None)
    
    




if __name__=="__main__":
        app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)