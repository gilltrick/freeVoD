from flask import Flask, render_template, request, make_response, redirect
import re, math, database, analytics
from threading import Thread

cookiePattern = re.compile("{\"username\":\"(.*)\";\"password\":\"(.*)\"}")
app = Flask(__name__)

@app.route("/")
def index():
    totalRecordsCount = str(len(database.fullList))
    resultCount = 0
    return render_template("home.html", resultCount=resultCount, totalRecordsCount=totalRecordsCount, popularCategoriesList=database.GetPopularCategoriesList(), popularActorList=database.GetPopularActorList())

@app.route("/home")
def home():
    totalRecordsCount = str(len(database.fullList))
    resultCount = 0
    return render_template("home.html", resultCount=resultCount, totalRecordsCount=totalRecordsCount, popularCategoriesList=database.GetPopularCategoriesList(), popularActorList=database.GetPopularActorList())

@app.route("/index")
def INDEX():
    totalRecordsCount = str(len(database.fullList))
    return render_template("index.html", resultCount=0, totalRecordsCount=totalRecordsCount, popularCategoriesList=database.GetPopularCategoriesList(), popularActorList=database.GetPopularActorList())

@app.route("/loginUser", methods=["post"])
def loginUser():
    username = request.form["username"]
    password = request.form["password"]
    print("DEBGU: freevod.py login attempt >> ", username, password)
    if database.userDatabase.CheckCredentials(username, password) == True:
        resultCount = 0
        cookieValue = "{\"username\":\""+username+"\";\"password\":\""+password+"\"}"
        keyWords = "-selected"
        keyWordsList = re.split("\s+", keyWords)
        mioList = database.SearchByKeyword(keyWordsList)
        maxPageCount = math.ceil(len(mioList)/32)
        pageCounter = 1
        resultCount = 32
        if len(mioList) < 32:
            resultCount = len(mioList)  
        response = make_response(render_template("home.html", mioList=mioList, pageCounter=pageCounter, maxPageCount=maxPageCount, resultCount=resultCount, keyWords=keyWords))
        response.set_cookie("data", cookieValue)
        return response
    metaInformationObject = database.modules.MetaInformationObject()
    metaInformationObject.videoUrl = "/static/data/__/ahahah_low.mp4"
    metaInformationObject.videoTitle = "You didn't say the magic word"
    metaInformationObject.discription = "To watch the clip you want you need to be loged in"
    return render_template("videoPlayer.html", metaInformationObject=metaInformationObject)
        
@app.route("/search", methods=["post"])
def search():
    keyWords = request.form["keyWords"]
    keyWordsList = re.split("\s+", keyWords)
    mioList = database.SearchByKeyword(keyWordsList)
    Thread(target=analytics.SaveKeyWordList(keyWordsList))
    Thread(target=analytics.UpdateCategoryObject(keyWords))
    Thread(target=analytics.UpdateActorObject(keyWords))
    resultCount = 32
    if len(mioList) < 32:
        resultCount = len(mioList)
    pageCounter = 1
    maxPageCount = math.ceil(len(mioList)/32)
    if len(mioList) < 1:
        return render_template("home.html", resultCount=0, popularCategoriesList=database.GetPopularCategoriesList(), popularActorList=database.GetPopularActorList())
    return render_template("home.html", mioList=mioList, pageCounter=pageCounter, maxPageCount=maxPageCount, resultCount=resultCount, keyWords=keyWords)

@app.route("/redirect", methods=["post"])
def Redirect():
    url = request.form["url"]
    print("DRAGONBALL: URL: " + url)
    analytics.AnalyticalObjectExits(url)
    return redirect(url)

@app.route("/page", methods=["post"])
def page():
    keyWords = request.form["keyWords"]
    pageCounter = int(request.form["pageCounter"])
    command = request.form["command"]
    keyWordsList = re.split("\s+", keyWords)
    mioList = database.SearchByKeyword(keyWordsList)
    maxPageCount = math.ceil(len(mioList)/32)
    if command == "nextPage":
        for i in range(32*pageCounter):
            mioList.remove(mioList[0])
        pageCounter += 1
    if command =="prevPage":
        pageCounter -= 1
        for i in range(32*(pageCounter-1)):
            mioList.remove(mioList[0])   
    resultCount = 32
    if len(mioList) < 32:
        resultCount = len(mioList)        
    return render_template("home.html", mioList=mioList, pageCounter=pageCounter, maxPageCount=maxPageCount, resultCount=resultCount, keyWords=keyWords)

@app.route("/playVideo", methods=["post"])
def videoPlayer():
    url = request.form["videoUrl"]
    if url == "":
        return "error"
    if "special" in url:
        metaInformationObject = database.GetMetaInfromationObjectByVideoUrl(url)
        if metaInformationObject.origin == "free":
            analytics.AnalyticalObjectExits(url)
            return render_template("videoPlayer.html", metaInformationObject=metaInformationObject)
        
        cookieValue = request.cookies.get("data")
        username, password = GetCookieData(cookieValue)
        if database.userDatabase.CheckCredentials(username, password) == True:
            if metaInformationObject == "invalid":
                return "ERROR"
            return render_template("videoPlayer.html", metaInformationObject=metaInformationObject)
        metaInformationObject = database.CreateDummyObject()
        return render_template("videoPlayer.html", metaInformationObject=metaInformationObject)
    metaInformationObject = database.GetMetaInfromationObjectByVideoUrl(url)
    analytics.AnalyticalObjectExits(url)
    if metaInformationObject == "invalid":
        metaInformationObject = database.CreateDummyObject()
        return render_template("videoPlayer.html", metaInformationObject=metaInformationObject)
    return render_template("videoPlayer.html", metaInformationObject=metaInformationObject)        

@app.route("/login")
def login():
    return render_template("login.html")

def GetCookieData(_cookieValue):
    if _cookieValue == None:
        return "",""
    result = re.search(cookiePattern, _cookieValue)
    username = result.group(1)
    password = result.group(2)
    return username, password

@app.route("/upVote", methods=["post"])
def upVote():
    id = request.form["upVote"]
    database.UpdateMetaInformationObject(id, "upVote", 1)
    return "<script>alert(\"Thanks for your vote!.\");location.href = \"/\";</script>" 

@app.route("/downVote", methods=["post"])
def downVote():
    id = request.form["upVote"]
    database.UpdateMetaInformationObject(id, "downVote", 1)
    return "<script>alert(\"Thanks for your vote!.\");location.href = \"/\";</script>" 

@app.route("/impressum")
def impressum():
    return render_template("impressum.html")    

@app.route("/freeSample")
def add():
    metaInformationObject = database.GetMetaInformationObjectById("eeb0f9991f46a8293558e3103ecf594e")
    analytics.AnalyticalObjectExits(metaInformationObject.videoUrl)
    return render_template("videoPlayer.html", metaInformationObject=metaInformationObject) 

@app.route("/sendComment", methods=["post"])
def sendComment():
    videoId = request.form["videoId"]
    commentContent = request.form["commentContent"]
    writerName = request.form["witerName"]
    database.AddComment(videoId, commentContent, writerName)
    metaInformationObject = database.GetMetaInformationObjectById(videoId)
    return render_template("videoPlayer.html", metaInformationObject=metaInformationObject)

@app.route("/register", methods=["post"])
def register():
    command = request.form["command"]
    return "currently deactivated"

@app.route("/registerUser", methods=["post"])
def registerUser():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]
    #database.userDatabase.CreateUser(username, password, email)
    return "currently deactivated"

@app.route("/forgottPassword", methods=["post"])
def forgottPassword():
    command = request.form["command"]
    return "currently deactivated"
    
if __name__ == "__main__":
    database.InitDatabase()
    app.run(debug=True, host="0.0.0.0", port=5005)