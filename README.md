![](https://github.com/rbnphlp/HolidayStories/blob/master/static/img/Updatedresponsive.png)	
# Web app to add & share your future holidays


The project as part of Module3:Code Institute is an attempt to allow user .


Backend built on MongoDB , with AmazonS3 for Picture Storage and Flask Frame work.
UI is built on Materialise Framework.



## UX Design 

+ The Skeleton Layout:


    - A HomePage : Page explaining User needs and Web app Goals  
    - Holiday Tales Page : Page to display initial cover Images of Holidays along with a Title , likes & No of Images uploaded   
    - Add a Holiday : A form page which allows users to add Holidays with a Title and Description (available as FAB at the bottom of page)
    - Add  Memories : A fom page which allows users to add Memories with Title and Description (available as FAB at the bottom of page)
    - Subsuquent Edit and Delete Pages from the above
    - Memories : Page displaying a carousel of Memories in a card image

Initial wireframe used for developing a prototype :

> ![](https://github.com/rbnphlp/HolidayStories/blob/master/Wire_frame_Holiday_Stories%402x-1.png)	



## DB Design 

+ The MongoDb had two collections , Holidays and Memories :
    - Holidays Collection simply containg the title and Destination along with upvotes info
    - Memories Collection had the corresponding memory title , description , image url link along with each memory referencing the Holidays Collection by the unique        id.This allowed , to keep the Memories collection relatively small  and well within limit of 16MB for future uploads
    - Images are uploaded initially captured from form uploads , processed and uploaded to s3 using boto3.The corresponding link is then inserted along with form aguments to MongoDB for future retrieval. Any additional image uploaded for a same memory  will simply be replaced with the most recent image. And hence , Each Memory has one image with each holiday having multiple Memories.

    


> ![](https://github.com/rbnphlp/HolidayStories/blob/master/Screenshot%20from%202020-08-23%2017-40-51.png)	



## User Stories

> "*I want to see others who visited a destination I am instrested in for a holiday , and things they did* "

> "*I want to share my holiday memories  for others to feedback * "

> "*I  want a collage of memories of my favourite Holidays which tells a story *"


## Design 


The Web-Pages are designed to make easy  add and share holiday memories and Images with little effort.


+ Features Added: 
    - Allow Users Add Holidays with a Title & Destination 
    - Allow Users to Add Memories for Each holidays
    - Allow Users to Add Images for each Memory along with short , titles and descriptions
    - Allows users to edit and Delete Memories 
    - Allow users to delete Holidays from Mongo-db
    - Allow users to up-vote Holidays they are intrested in
    

+ Features Not Implemented or nice to Haves :
    - Pagination 
    - Search bar based on Country,Date etc
    - USer profiles
    - A comment section




## Technologies :


### Languages:

+ HTML
+ CSS
+ Javascript
+ Python (Flask , boto3, jinja, json)
+ Mongo-db
    
### Libraries /Frameworks:
+ Materialise
+ Jquery
+ MaterialIcons

  
## Testing :



+ Header & Navigation bar :
     - Href links to correct elements -checked and working
     - Nav Bar correcly alligned for Desktop Version only ! 
     - NAv bar side display added for Mobile Version
     


+ Body  :
     - Loaded Holidays Page in  (Safari,Firefox and Chrome)
     - Works well in Desktop versions , Allignment issues when Title is long in Holidays Page for Laptop + Mobile views
     - Memories Page compatible in all views , however carousel is sometime non-responsive  on mobile versions
     - Forms render well in all views , buttons however too big fo mobile view.
     
+
            
     
+ Full web page checks : 
     - Tested all of the above on desktop (firefox and chrome) - *Other Screen sizes not implemented*
     - Ran the web page for any html/css errors on https://validator.w3.org/ - issues with closing a tags

     
### Bug Fixes (Open & Closed) :


| Bug-Location      | Bug-Type  | Bug-Status|
| ------------- |:-------------:| ---------:|
|  view_jolidays.html   |  html-validation error | Fixed |
|  view_memories.html   |  html-validation error   |  Fixed |
|  Various routes in Flask (Add_memories )|   logic |  Fixed |
|   css &html |   Resposniveness - Carousel sometimes not responsive on mobile  |  Open |

## Deployment

The Web pages was deployed through following :
+  Setting up a heroku app with login.
+ adding files through git remote 
+ made sure all keys + access keys were deleted and any accidentally uplodaded keys were rotated to new ones .All config variables were set to enviornment variables using Heroku set CLI and using a pylib dot env to read the env variables.
+ Build process through git remote heroku and push





## Acknowledgements
 Thanks for Code institute and their awesome tutor support team along with my mentor :)
 













