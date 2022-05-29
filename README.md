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
