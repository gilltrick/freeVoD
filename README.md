
Get Started

    #Install the app and downloading rquirements from requirements.txt
    python setup.py
    #Run the server
    python freeVoD.py
    Enter command: "-start"
    #Visit your new tube
    http://localhost:5005

Setup New Database

    #Setup your local database for video content
    python freeVoD.py
    #Access the database
    python freeVoD.py
    Enter command: "-database"
    #Copy video content to /input/ folder
    Enter command: "-addall"
    #Wipe existing data
    Enter command: "-yes"


Convert Media

    #FFMPEG is used to covert the data
    python freeVoD.py
    #Start converter
    Enter command: "-converter"
    #Converted files are in /output/ folder


Set up a users

    #Add a user to database
    python freeVoD.py
    #Access the user database
    Enter command: "-userDatabase"
    #Create a new user
    Enter command : "-newUser"
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
