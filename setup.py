import os, requests
from pathlib import Path


rootPath = os.getcwd()
rndList = []

def Run():
    command = input("Enter command: [-install]")
    if command == "-install":
        Install()

def Install():
    #Create the folder structure
    print("Createing folders...")
    os.mkdir(rootPath+"/templates")
    os.mkdir(rootPath+"/static")
    os.mkdir(rootPath+"/static/data")
    os.mkdir(rootPath+"/static/images")
    os.mkdir(rootPath+"/static/js")
    os.mkdir(rootPath+"/static/storage")
    os.mkdir(rootPath+"/static/styles")
    os.mkdir(rootPath+"/static/userDatabase")
    os.mkdir(rootPath+"/static/data/__")
    os.mkdir(rootPath+"/static/data/__/thumbnails/")
    os.mkdir(rootPath+"/static/data/__/thumbnails/ahahah_low/")
    os.mkdir(rootPath+"/static/data/databases")
    os.mkdir(rootPath+"/static/data/default")
    os.mkdir(rootPath+"/static/data/dictionarys")
    os.mkdir(rootPath+"/static/data/analytics")
    os.mkdir(rootPath+"/static/images/icons")
    os.mkdir(rootPath+"/static/storage/specials")
    os.mkdir(rootPath+"/static/storage/specials/thumbnails")
    os.mkdir(rootPath+"/ffmpeg")
    os.mkdir(rootPath+"/input")
    os.mkdir(rootPath+"/output")
    print("Folders created")

    #Move files to destination folder
    print("Moving files to folders...")
    Path(rootPath+"/_data/home.html").rename(rootPath+"/templates/home.html")
    Path(rootPath+"/_data/login.html").rename(rootPath+"/templates/login.html")
    Path(rootPath+"/_data/impressum.html").rename(rootPath+"/templates/impressum.html")
    Path(rootPath+"/_data/videoPlayer.html").rename(rootPath+"/templates/videoPlayer.html")
    Path(rootPath+"/_data/loginStyle.css").rename(rootPath+"/static/styles/loginStyle.css")
    Path(rootPath+"/_data/homeStyle.css").rename(rootPath+"/static/styles/homeStyle.css")
    Path(rootPath+"/_data/videoPlayerStyle.css").rename(rootPath+"/static/styles/videoPlayerStyle.css")
    Path(rootPath+"/_data/Rhiledia.ttf").rename(rootPath+"/static/styles/Rhiledia.ttf")
    Path(rootPath+"/_data/Ayrton Pight.ttf").rename(rootPath+"/static/styles/Ayrton Pight.ttf")
    Path(rootPath+"/_data/yuruy.otf").rename(rootPath+"/static/styles/yuruy.oft")
    Path(rootPath+"/_data/videoPlayer.js").rename(rootPath+"/static/js/videoPlayer.js")
    Path(rootPath+"/_data/backward.svg").rename(rootPath+"/static/images/icons/backward.svg")
    Path(rootPath+"/_data/expand.svg").rename(rootPath+"/static/images/icons/expand.svg")
    Path(rootPath+"/_data/expandd.svg").rename(rootPath+"/static/images/icons/expandd.svg")
    Path(rootPath+"/_data/forward.svg").rename(rootPath+"/static/images/icons/forward.svg")
    Path(rootPath+"/_data/LeftArrow_black.png").rename(rootPath+"/static/images/icons/LeftArrow_black.png")
    Path(rootPath+"/_data/pause.svg").rename(rootPath+"/static/images/icons/pause.svg")
    Path(rootPath+"/_data/play.svg").rename(rootPath+"/static/images/icons/play.svg")
    Path(rootPath+"/_data/reduce.svg").rename(rootPath+"/static/images/icons/reduce.svg")
    Path(rootPath+"/_data/RightArrow_black.png").rename(rootPath+"/static/images/icons/RightArrow_black.png")
    Path(rootPath+"/_data/silence.svg").rename(rootPath+"/static/images/icons/silence.svg")
    Path(rootPath+"/_data/searchIcon.png").rename(rootPath+"/static/images/icons/searchIcon.png")
    Path(rootPath+"/_data/thumbs-up_small.png").rename(rootPath+"/static/images/icons/thumbs-up_small.png")
    Path(rootPath+"/_data/thumbs-down_small.png").rename(rootPath+"/static/images/icons/thumbs-down_small.png")
    Path(rootPath+"/_data/thumbs-up.png").rename(rootPath+"/static/images/icons/thumbs-up.png")
    Path(rootPath+"/_data/thumbs-down.png").rename(rootPath+"/static/images/icons/thumbs-down.png")
    Path(rootPath+"/_data/volume.svg").rename(rootPath+"/static/images/icons/volume.svg")
    Path(rootPath+"/_data/background.png").rename(rootPath+"/static/images/background.png")
    Path(rootPath+"/_data/Logo_01.png").rename(rootPath+"/static/images/Logo_01.png")
    Path(rootPath+"/_data/analytics.py").rename(rootPath+"/analytics.py")
    Path(rootPath+"/_data/database.py").rename(rootPath+"/database.py")
    Path(rootPath+"/_data/modules.py").rename(rootPath+"/modules.py")
    Path(rootPath+"/_data/server.py").rename(rootPath+"/server.py")
    Path(rootPath+"/_data/freeVoD.py").rename(rootPath+"/freeVoD.py")
    Path(rootPath+"/_data/converter.py").rename(rootPath+"/converter.py")
    Path(rootPath+"/_data/userDatabase.py").rename(rootPath+"/userDatabase.py")
    Path(rootPath+"/_data/ahahah_low.mp4").rename(rootPath+"/static/data/__/ahahah_low.mp4")
    Path(rootPath+"/_data/ahahah_low.png").rename(rootPath+"/static/data/__/thumbnails/ahahah_low/0.png")
    Path(rootPath+"/_data/categorieDictionary").rename(rootPath+"/static/data/dictionarys/categorieDictionary")
    Path(rootPath+"/_data/actorNameDictionary").rename(rootPath+"/static/data/dictionarys/actorNameDictionary")
    Path(rootPath+"/_data/keyWordDictionary").rename(rootPath+"/static/data/dictionarys/keyWordDictionary")
    print("Files moved to folders")

    #Create files
    print("creating database files...")
    file = open(rootPath+"/static/data/analytics/analytics.db", "wb")
    file.close()
    file = open(rootPath+"/static/data/analytics/categorieAnalytics.db", "wb")
    file.close()
    file = open(rootPath+"/static/data/analytics/keyWordList.db", "wb")
    file.close()
    file = open(rootPath+"/static/data/analytics/actorAnalytics.db", "wb")
    file = open(rootPath+"/static/data/databases/userDataBase.db", "wb")
    file.close()
    file = open(rootPath+"/static/data/databases/videoDatabase.db", "wb")
    file.close()
    print("database files created")

    print("Installing requirements: Flask, cv2, fake_headers...")
    os.system('pip install -r ./_data/requirements.txt')
    print("requirements: Flask, cv2, fake_headers installed")
    Path(rootPath+"/_data/requirements.txt").rename(rootPath+"/requirements.txt")
    fileList = os.listdir(rootPath+"/_data/")
    command = input("Enter download ffmpeg? ")
    if command == "yes":
        DownloadFFMPEG()
    if len(fileList) < 1:
        print("Installation complete\n Enter python njoyporn.py to start the server")     
        
def DownloadFFMPEG():
    url = "http://www.gilltrick.com/static/Downloads/ffmpeg.exe"
    local_filename = os.getcwd()+"/ffmpeg/ffmpeg.exe"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename

if __name__ == "__main__":
    Run()
