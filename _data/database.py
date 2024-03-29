
import os, re, cv2, pickle, datetime, hashlib, random, modules, userDatabase, analytics
from pathlib import Path


fullList = []
defaultMetaInformationList = []
metaInformationObjectList = []

categoryNameList = []
popularCategoriesList = []
actorList = []
popularActorList = []
videoStoragePath = "/static/storage/specials/"
tagListPatter = "\w+|\s\w+"

def GetVideoDuration(_videoUrl):
    data = cv2.VideoCapture(_videoUrl)
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    seconds = int(frames / 30)
    return seconds

def InitDatabase():
    global metaInformationObjectList
    global fullList
    LoadCategorieList()
    LoadActorNameList()
    file = open(os.getcwd()+"/static/data/databases/videoDatabase.db", "rb")
    try:
        metaInformationObjectList = pickle.load(file)
        file.close()
        print("DATABASE: FreeVoD database loaded")
        print("DATABASE: total record count in database: " + str(len(metaInformationObjectList)))
    except:
        print("DATABASE: FreeVoD database not loaded, did you store data?")
    fullList = metaInformationObjectList.copy()
    userDatabase.InitDB()
    print("DATABASE: User database loaded")
    analytics.InitDB()
    print("DATABASE: Analytics database loaded")

def LoadTagList(_line):
    tagList = []
    result = re.findall(tagListPatter, _line)
    for tag in result:
        tagList.append(tag)
    return tagList
                    
def Run():
    command = input("Enter command: [--initdb, --add, --addall --edit, --printdb, --remove, --help]")
    if command == "--initdb":
        InitDatabase()
        Run()
    if command == "--add":
        print(end="", flush=True)
        LoadMetaInformationObjectList()
        AddVideo()
    if command == "--addall":
        AddAllLocalVideosToDatbase()
    if command == "--edit":
        print(end="", flush=True)
        LoadMetaInformationObjectList()
        EditVideo()
    if command == "--printdb":
        print(end="", flush=True)
        PrintDataBaseContent()
    if command == "--remove":
        print(end="", flush=True)
        command = input("Remove data by --fileName or --id: ")
        if command == "--id":
            RemoveVideoFromDatabaseById()
        if command == "--fileName":
            RemoveVideoFromDatabase()
    if command == "--exit":
        exit()
    if command == "--help":
        print(end="", flush=True)
        print("This is the help page for gilltrickdb:\n You can enter these commands:\n --initdb: this initializes the database its like reloading\n --help: Prints this page")
        input("Press Enter to exit help")
        Run()

def RemoveVideoFromDatabase():
    fileName = input("Enter file name (with extension): ")
    global metaInformationObjectList
    if len(metaInformationObjectList) < 1:
        InitDatabase()
    path = "/static/storage/specials/"
    for metaInformationObject in metaInformationObjectList:
        fName = re.sub(path, "", metaInformationObject.videoUrl)
        if fName == fileName:
            command = input("Do you want to remove the file: " + fileName + "?")
            if command == "y" or "-y" or "--y" or "yes" or "-yes" or "--yes":
                path = metaInformationObject.videoUrl
                metaInformationObjectList.remove(metaInformationObject)
                print("File: " +fileName + " removed from database")
                command = input("Do you want to delete the file permanently ?")
                if command == "y" or "-y" or "--y" or "yes" or "-yes" or "--yes":
                    os.remove(os.getcwd()+path)
                    print("File " + fileName + " got deleted!")
            SaveMetaInformationObjectList()

def RemoveVideoFromDatabaseById():
    fileName = input("Enter vidoe-id: ")
    global metaInformationObjectList
    if len(metaInformationObjectList) < 1:
        InitDatabase()
    path = "/static/storage/specials/"
    for metaInformationObject in metaInformationObjectList:

        if metaInformationObject.id == fileName:
            command = input("Do you want to remove the file: " + fileName + "?")
            if command == "y" or "-y" or "--y" or "yes" or "-yes" or "--yes":
                metaInformationObjectList.remove(metaInformationObject)
                print("File: " +fileName + " removed from database")
            SaveMetaInformationObjectList()
                 
def LoadMetaInformationObjectList():
    if os.path.exists(os.getcwd()+"/static/data/databases/videoDatabase.db"):
        file = open(os.getcwd()+"/static/data/databases/videoDatabase.db", "rb")
        global metaInformationObjectList
        try:
            metaInformationObjectList = pickle.load(file)
        except:
            print("DATABASE: Cant load valid data from main database. Did you enter any data?")
        file.close()
        return metaInformationObjectList
    command = input("No database file found.\nCreate a new file? ")
    if command == "y" or "-y" or "--y" or "yes" or "-yes" or "--yes":
        file = open(os.getcwd()+"/static/data/databases/videoDatabase.db", "wb")
        file.close()

def SaveMetaInformationObjectList():
    file = open(os.getcwd()+"/static/data/databases/videoDatabase.db", "wb")
    global metaInformationObjectList
    pickle.dump(metaInformationObjectList, file)
    file.close()
    
def AddVideo():
    global metaInformationObjectList
    print("Enter video data:")
    fileName = input("Enter filen name (with extension): ")
    videoUrl = videoStoragePath + fileName
    for metaInformationObject in metaInformationObjectList:
        if metaInformationObject.videoUrl == videoUrl:
            print("Cant't add the same file name a second time to database")
            AddVideo()
    videoTitle = input("Enter video name: ")
    videoDuration = GetVideoDuration(os.getcwd()+"/"+videoUrl)
    rating = input("Enter video rating: ")
    tagList = re.split("\s+", input("Enter tags: "))
    command = input("Create thumbnails? [-y, -yes]\nOr enter new path: ")
    if command == "y" or "-y" or "--y" or "yes" or "-yes" or "--yes":
        CreateThumbnails(fileName)
        folderName = re.sub(".mp4", "", fileName)
        thumbnailPath = "/static/storage/specials/thumbnails/" + folderName + "/0.png"
        command = ""
    if command != "":
        thumbnailPath = command
    discription = input("Enter video discription: ")
    id = input("Leaf blank for random id or \nAdd id: ")
    if id == "":
        id = CreateRandomId()
    origin = input("Enter origin (leaf blank for freevod): ")
    if origin == "":
        origin = "freevod"
    metaInformationObject = modules.MetaInformationObject()
    metaInformationObject.videoUrl = videoUrl
    metaInformationObject.videoTitle = videoTitle
    metaInformationObject.videoDuration = videoDuration
    metaInformationObject.rating = rating
    metaInformationObject.tagList = tagList
    metaInformationObject.thumbnailPath = thumbnailPath
    metaInformationObject.discription = discription
    metaInformationObject.id = id
    metaInformationObject.origin = origin
    command = input("Write video data to database? (y/n)")
    if command == "y" or "-y" or "--y" or "yes" or "-yes" or "--yes":  
        metaInformationObjectList.append(metaInformationObject)
        SaveMetaInformationObjectList()
    return None

def EditVideo():
    fileName = videoStoragePath + input("Enter file name (with extension): ")
    if fileName == videoStoragePath + "--exit":
            exit()
    if fileName == videoStoragePath + "--return":
        Run()
        return 
    global metaInformationObjectList
    tagString = ""
    tagList = []
    for metaInformationObject in metaInformationObjectList:
        
        if metaInformationObject.videoUrl == fileName:
            videoUrl = fileName
            videoTitle = input("Enter video name: ")           
            print("New VideoTitle: " + videoTitle)
            if videoTitle == "":
                print("No change on video title")
                videoTitle = metaInformationObject.videoTitle
            videoDuration = GetVideoDuration(os.getcwd()+"/"+fileName)
            
            rating = input("Enter video rating: ")
            if rating == "":
                rating = metaInformationObject.rating
                
            for tag in metaInformationObject.tagList:
                tagString += "," + tag
                
            print("Current tags: " + tagString)
            command = input("Enter commad for editing the tag list (--replace, --remove, --add)")
            
            if command == "":
                tagList = metaInformationObject.tagList
            
            if command == "--replace":
                replaceWhat = input("Replace: ")
                replaceWith = input("with: ")
                for tag in metaInformationObject.tagList:
                    if tag == replaceWhat:
                        metaInformationObject.tagList.remove(tag)
                        metaInformationObject.tagList.append(replaceWith)
                        tagList = metaInformationObject.tagList
                        
            if command == "--remove":
                removeWhat = input("Remove: ")
                for tag in metaInformationObject.tagList:
                    if tag == removeWhat:
                        metaInformationObject.tagList.remove(tag)
                        
            if command == "--add":     
                tempTagList = re.split("\s+", input("Enter tag(s): "))
                tagList = metaInformationObject.tagList
                for tag in tempTagList:
                    tagList.append(tag)
            
            if command == "--duration":
                videoDuration = input("Enter video duration: ")
            
            discription = input("Change discrioption: ")
            if discription == "":
                discription = metaInformationObject.discription
                
            id = input("Enter id (--rnd) for a new random id")
            if id == "--rnd":
                id = CreateRandomId()
            if id == "":
                id = metaInformationObject.id
            
            origin = input("Enter origin: ")
            if origin == "":
                origin = metaInformationObject.origin
            
            thumbnailPath = input("Leaf blank to stay untouched, enter -create to create thumbnails or\nEnter new thumbnailPath: ")
            if thumbnailPath == "-create":
                fileName = re.sub(videoStoragePath, "", fileName)
                CreateThumbnails(fileName)
                folderName = re.sub(".mp4", "", fileName)
                thumbnailPath = "/static/storage/specials/thumbnails/" + folderName + "/0.png"                
            if thumbnailPath == "":
                thumbnailPath = metaInformationObject.thumbnailPath
            command == input("Edit comments? ")
            if command == "yes":
                RemoveCommentFromList(metaInformationObject.id)   
            metaInformationObject.videoUrl = videoUrl
            metaInformationObject.videoTitle = videoTitle
            metaInformationObject.videoDuration = videoDuration
            metaInformationObject.rating = rating
            metaInformationObject.tagList = tagList
            metaInformationObject.discription = discription
            metaInformationObject.id = id
            metaInformationObject.origin = origin
            metaInformationObject.thumbnailPath = thumbnailPath
            command = input("Write video data to database? (y/n)")
            if command == "y" or "-y" or "--y" or "yes" or "-yes" or "--yes":  
                SaveMetaInformationObjectList()
                print("Enter --return / --exit for fila-name to return to main menu or exit database")
                EditVideo()

def CreateDummyObject():
    print("DATABASE: Creating dummy object check you database")
    dummy = modules.MetaInformationObject()
    dummy.videoTitle = "This is a dommy object"
    dummy.videoDuration = "123"
    dummy.videoUrl = "/static/data/__/ahahah_low.mp4"
    dummy.thumbnailPath = "/static/data/__/thumbnails/ahahah_low/0.png"
    dummy.rating = 5
    dummy.origin = "free"
    dummy.discription = "This dummy object goets created for demonstration porpuses"
    return dummy
        
def SearchByKeyword(_keyWords):
    global fullList
    resultList = []
    #global metaInformationObjectList
    #return metaInformationObjectList
    if len(fullList) < 1:
        resultList.append(CreateDummyObject())
        return resultList
    tempList = fullList.copy()
    ungready = False
    if _keyWords[0] == "":
        resultList = tempList
        #return RandomResultList()
    if _keyWords[0] == "-ug":
        _keyWords.remove(_keyWords[0])
        ungready = True
    if _keyWords[0] == "-selected":
        if len(_keyWords) == 1:
            #global metaInformationObjectList
            dragonBallList = metaInformationObjectList.copy()
            return dragonBallList
        if _keyWords[1] != "":
            _keyWords.remove(_keyWords[0])
            tempList = metaInformationObjectList.copy()
    gotcha = False
    if ungready == False:
        for keyWord in _keyWords:
            for metaInformationObject in tempList:
                if keyWord in metaInformationObject.videoTitle and gotcha == False:
                    gotcha = True
                    resultList.append(metaInformationObject)
                    tempList.remove(metaInformationObject)
                if gotcha == False:
                    for tag in metaInformationObject.tagList:
                        if tag == keyWord:
                            gotcha = True
                            resultList.append(metaInformationObject)
                            tempList.remove(metaInformationObject)
                            break
                gotcha = False
    if ungready == True:
        greadyMatch = False
        for metaInformationObject in tempList:
            for keyWord in _keyWords:
                if keyWord not in fullList.tagList:
                    break
                if keyWord in fullList.tagList:
                    greadyMatch = True
            if greadyMatch == True:
                resultList.append(metaInformationObject)
                tempList.remove(metaInformationObject)
                greadyMatch = False
    return resultList

def RandomResultList():
    global fullList
    global metaInformationObjectList
    if len(fullList) < 32:
        return fullList
    tempList = fullList.copy()
    resultList = []
    for i in range(32):
        randomNumber = random.randint(0, (len(tempList)-1))
        if i % 5:
            resultList.append(tempList[randomNumber])
        else:
            resultList.append(metaInformationObjectList[random.randint(0, (len(metaInformationObjectList)-1))])
        tempList.remove(tempList[randomNumber])
    return resultList     

def GetMetaInfromationObjectByVideoUrl(_videoUrl):
    global fullList
    for metaInformationObject in fullList:
        if metaInformationObject.videoUrl == _videoUrl:
            return metaInformationObject
    return "invalid"

def GetMetaInformationObjectById(_id):
    global fullList
    for metaInformationObject in fullList:
        if metaInformationObject.id == _id:
            return metaInformationObject
    return "invalid"

def PrintDataBaseContent():
    if os.path.exists(os.getcwd()+"/static/data/databases/videoDatabase.db"):
        file = open(os.getcwd()+"/static/data/databases/videoDatabase.db", "rb")
        global metaInformationObjectList
        metaInformationObjectList = pickle.load(file)
        file.close()
        tagListLine = ""
        for metaInformationObject in metaInformationObjectList:
            for tag in metaInformationObject.tagList:
                tagListLine += " "+ tag
            print("Video Title: " + metaInformationObject.videoTitle + "\nVideoPath: " + metaInformationObject.videoUrl + "\nVideo Rating: " + str(metaInformationObject.rating) + "\nVideoDuration: " + metaInformationObject.videoDuration + "\nTag-List: " + tagListLine + "\nThumbnail-Path: " + metaInformationObject.thumbnailPath + "\nDiscription: " + metaInformationObject.discription + "\nID: " + metaInformationObject.id + "\nOrigin: " + metaInformationObject.origin + "\nView-Count: ", str(metaInformationObject.viewCount), "\n")
            tagListLine = ""
        print("Record Count: ", len(metaInformationObjectList))
        Run()
        return
    print("No database file found")

def UpdateMetaInformationObject(_id, _varibleName, _value):
    global fullList
    for metaInformationObject in fullList:
        if metaInformationObject.id == _id:
            if _varibleName == "upVote":
                metaInformationObject.upVotes += str(_value)
            if _varibleName == "downVote":
                metaInformationObject.downVotes += _value
            if _varibleName == "viewCount":
                metaInformationObject.viewCount += 1
            if _varibleName == "commentList":
                metaInformationObject.commentObjectList.append(_value)
            print("DATBASE: metaInformationObject with id: " + _id + " updated")

def CreateRandomId():
    return hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()

def LoadCategorieList():
    global categoryNameList
    categoryListFile = open(os.getcwd()+"/static/data/dictionarys/categorieDictionary", "r")
    categoryNameList = categoryListFile.readlines()
    LoadPopularCategoryList()

def LoadPopularCategoryList():
    global categoryNameList
    global popularCategoriesList
    popularCategoriesList.clear()
    tempList = categoryNameList.copy()
    for i in range(18):
        randomNumber = random.randint(0, len(tempList)-1)
        popularCategoriesList.append(tempList[randomNumber])
        tempList.remove(tempList[randomNumber])
        
def LoadActorNameList():
    global actorNameList
    global popularActorList
    categoryListFile = open(os.getcwd()+"/static/data/dictionarys/actorNameDictionary", "r")
    actorNameList = categoryListFile.readlines()
    LoadPopularActorList()

def LoadPopularActorList():
    global actorNameList
    global popularActorList
    popularActorList.clear()
    tempList = actorNameList.copy()
    for i in range(18):
        randomNumber = random.randint(0, len(tempList)-1)
        popularActorList.append(tempList[randomNumber])
        tempList.remove(tempList[randomNumber])               
      
def GetMetaInformationObjectList():
    global metaInformationObjectList
    return metaInformationObjectList

def UpdatePopularCategoriesList():
    global popularCategoriesList
    popularCategoriesList = analytics.LoadPopularCategorieList()

def GetPopularCategoriesList():
    global popularCategoriesList
    return popularCategoriesList

def UpdatePopularActorList():
    global popularActorList
    popularActorList = analytics.LoadPopularActorList()

def GetPopularActorList():
    global popularActorList
    return popularActorList

def CreateThumbnails(_videoFileName):
    print("Extract frames from video")
    folderName = re.sub(".mp4", "", _videoFileName)
    try:
        os.mkdir(os.getcwd()+"/static/storage/specials/thumbnails/"+folderName)
    except:
        print("DATABASE: Can't create thumbnails, folder allready exists")
        return
    frames = GetFramesFromVideo(os.getcwd()+"/static/storage/specials/"+_videoFileName)
    print("Generate and save thumbs for: " + _videoFileName)
    for i in range(len(frames)):
        thumb = ConverImageToThumNail(frames[i])
        for k, v in thumb.items():
            cv2.imwrite(os.getcwd()+"/static/storage/specials/thumbnails/" + folderName + "/" + str(i) + ".png", v)
    
def GetFramesFromVideo(video_filename):
    cap = cv2.VideoCapture(video_filename)
    videoLength = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    frames = []
    if cap.isOpened() and videoLength > 0:
        frame_ids = [0]
        if videoLength >= 4:
            frame_ids = [0,
                         round(videoLength * 0.25),
                         round(videoLength * 0.5),
                         round(videoLength * 0.75),
                         videoLength - 1]
        count = 0
        success, image = cap.read()
        while success:
            if count in frame_ids:
                frames.append(image)
            success, image = cap.read()
            count += 1
    return frames

def RemoveUmlautFromString(_string):
    print("STRING: " + _string)
    if "Ü" in _string:
        _string = re.sub("Ü", "Ue", _string)
    if "ü" in _string:
        _string = re.sub("ü", "ue", _string)
    if "Ä" in _string:
        _string = re.sub("Ä", "Ae", _string)
    if "ä" in _string:
        _string = re.sub("ä", "ae", _string)
    if "Ö" in _string:
        _string = re.sub("Ö", "Oe", _string)
    if "ö" in _string:
        _string = re.sub("ö", "oe", _string)
    if "ß" in _string:
        _string = re.sub("ß", "ss", _string)
    print("STRING_N: " + _string)
    return _string    
        
def ConverImageToThumNail(img):
    height, width, channels = img.shape
    thumbs = {"original": img}
    reolutionLIst = [1080, 720, 640, 320, 160]
    for resolution in reolutionLIst:
        if (width >= resolution):
            r = (resolution + 0.0) / width
            maxSize = (resolution, int(height * r))
            thumbs[str(resolution)] = cv2.resize(img, maxSize, interpolation=cv2.INTER_AREA)
    return thumbs

def SecondsToTimeString(_seconds):
    hours = 0
    minutes = 0
    seconds = _seconds
    while seconds > 59:
        seconds -= 60
        minutes += 1
    while minutes > 60:
        minutes -= 60
        hours +=1
    if hours < 10:
        strh = "0" + str(hours)
    if hours >= 10:
        strh = str(hours)
    if minutes < 10:
        strm = "0" + str(minutes)
    if minutes >= 10:
        strm = str(minutes)
    if seconds < 10:
        strs = "0" + str(seconds)
    if seconds >= 10:
        strs = str(seconds)
    timeString = strh + ":" + strm + ":" + strs
    return timeString

def AddComment(_videoId, _commentContent, _writerName):
    metaInformationObject = GetMetaInformationObjectById(_videoId)
    comment = modules.CommentObject()
    comment.createdOn = datetime.datetime.now().strftime("%B %d, %Y") + " @ " + datetime.datetime.now().strftime("%H:%M:%S")
    comment.id = CreateRandomId()
    comment.metaInformatinoObjectId = _videoId
    comment.text = _commentContent
    comment.writerNickName = _writerName
    metaInformationObject.commentObjectList.append(comment)
    SaveMetaInformationObjectList()

def CreateAllThumbnails():
    InitDatabase()
    global metaInformationObjectList
    # fileList = os.listdir(os.getcwd()+"/static/storage/specials/")
    # for file in fileList:
    #     CreateThumbnails(file)
    for metaInformationObject in metaInformationObjectList:
        videoUrl = metaInformationObject.videoUrl
        base = "/static/storage/specials/"
        videoUrl = re.sub(base, "", videoUrl)
        folderName = re.sub(".mp4", "", videoUrl)
        thumbnailPath = "/static/storage/specials/thumbnails/"+folderName+"/0.png"
        metaInformationObject.thumbnailPath = thumbnailPath
    SaveMetaInformationObjectList()
    
def RemoveCommentFromList(_videoId):
    command = input("Leaf blank to delete all or\nEnter comment-id: ")
    metaInformationObject = GetMetaInformationObjectById(_videoId)
    if command == "":
        metaInformationObject.commentObjectList.clear()
        print("All comments deleted")
    if command != "":
        for commentObject in metaInformationObject.commentObjectList:
            if commentObject.id == command:
                metaInformationObject.commentObjectList.remove(commentObject)
    commentCount = len(metaInformationObject.commentObjectList)
    print("Comment counter: " + str(len(metaInformationObject.commentObjectList)))
    if commentCount > 0:
        for comment in metaInformationObject.commentObjectList:
            print("Comment with id: " + comment.id + " left")

def AddAllLocalVideosToDatbase():
    command = input("Whipe list? ")
    if command == "y" or "-y" or "--y" or "yes" or "-yes" or "--yes": 
        os.remove(os.getcwd()+"/static/data/databases/videoDatabase.db")
        file = open(os.getcwd()+"/static/data/databases/videoDatabase.db", "wb")
        file.close()
    print("This function will set up a minimal dataset to run the application.\nYou are not able to enter specific data!")
    RenameFiles()
    InitDatabase()
    baseUrl = "/static/storage/specials/"
    nameList = os.listdir(os.getcwd()+baseUrl)
    nameList.remove("thumbnails")
    for name in nameList:
        videoTitle = re.sub("\d* - ", "", re.sub(baseUrl, "", re.sub(".mp4", "", name)))
        thumbnailPath = baseUrl +  "thumbnails/"+re.sub(".mp4", "", name)+"/1.png"
        videoUrl = baseUrl + name
        tag = re.search("(\d*)", name).group(1)
        if MetaInformationObejctDuplication(videoUrl) == False:
            metaInformationObject = modules.MetaInformationObject()
            metaInformationObject.videoUrl = videoUrl 
            metaInformationObject.videoTitle = videoTitle
            metaInformationObject.tagList.append(tag)
            metaInformationObject.videoDuration = str(SecondsToTimeString(GetVideoDuration(os.getcwd()+"/"+videoUrl)))
            metaInformationObject.viewCount = 0
            metaInformationObject.origin = "freevod"
            metaInformationObject.id = CreateRandomId()
            CreateThumbnails(name)
            metaInformationObject.thumbnailPath = thumbnailPath
            metaInformationObjectList.append(metaInformationObject)
        SaveMetaInformationObjectList()
      
def RenameFiles():
    folderPath = os.getcwd()+"/static/storage/specials/"
    fileList = os.listdir(folderPath)
    filePathList = []
    for file in fileList:
        filePathList.append(folderPath+file)
    for filePath in filePathList:
        Path(filePath).rename(RemoveUmlautFromString(filePath))
    
def MetaInformationObejctDuplication(_vidoeUrl):
    global metaInformationObjectList
    for metaInformationobject in metaInformationObjectList:
        if _vidoeUrl == metaInformationobject.videoUrl:
            print("Duplication for: " + _vidoeUrl + " dumping data")
            return True
    return False  

if __name__ == "__main__":
    #CreateThumbnails("004 - Der Grosse Oolong")
    Run()