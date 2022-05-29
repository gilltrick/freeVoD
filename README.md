<br>
Get Started
<br>
    #Install the app and downloading rquirements from requirements.txt
    python setup.py
    #Run the server
    python freeVoD.py
    #Visit your new tube
    http://localhost:5005
<br>
<br> 
Add Data to Database
<br> 
  #Copy data<br>
  Copy the video files to /static/storage/speacials/<br>
  Run: python freeVoD.py<br>
  Enter command: "-database"<br>
  Enter command: "-addall"<br>
  Enter command: "-yes"<br>
  <br>
Converter
<br>
  #Converter<br>
  Copy the video files to /input/<br>
  Run: python freeVoD.py<br>
  Enter command: "-converter"<br>
  #Converted files
  Converted files saved in /output/


Get started

    #Install the app and downloading rquirements from requirements.txt
    python setup.py
    #Run the server
    python freeVoD.py
    #Visit your new tube
    http://localhost:5005

Set up a local database:

    #Copy the content you want to serve to your /static/storage/specials/
    #Run the main database application in terminal
    python database.py
    #Initialize the database
    --initdb
    #Add a video to the database
    --add
    #Enter data for at least:
        filename
        video-title
        create the Thumbnails
        save database
    #Check for data
    --printdb
    #Restart the server

Set up a webscraped database:

    #Chose and run a module
    python modulename.py
    #Initialize the database
    -initdb
    #Simple Search:
    -search
        enter keywords
        enter depth
        wait for it to complete
        save database
    #Check for data
    -printdb
    #Restart the server

Set up a users

    #Run the userdatabase module
    python userdatabase.py
    #Initialize the database
    -initdb
    #Add a new user
    -newUser
        enter username
        enter password
        enter email

Analytics

    #Run the analytics module
    python analytics.py
    #Initialize the database
    -initdb
    #Print data if available
    -print
        -video
        -categorie
        -actors
        -analytics
