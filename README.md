
Get started

    #Install the app and downloading rquirements from requirements.txt
    python setup.py
    #Run the server
    python freeVoD.py
    Enter command: "-start"
    #Visit your new tube
    http://localhost:5005


Set up the database

  #Set up you database
  Copy the video files to /static/storage/speacials/
  Run: python freeVoD.py
  Enter command: "-database"
  Enter command: "-addall"
  Enter command: "-yes"



Convert files:

  #Converter<br>
  Copy the video files to /input/<br>
  Run: python freeVoD.py<br>
  Enter command: "-converter"<br>
  #Converted files
  Converted files saved in /output/

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
