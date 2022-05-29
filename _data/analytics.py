import os, re, datetime, hashlib, pickle, database, modules

analyticalObjectList = []
keyWordListList = []
categorieAnalyticObjectList = []
actorAnalyticObjectList = []

def Run():
    command = input("Enter command: [-initdb, -print, -help]")
    if command == "-initdb":
        InitDB()
        Run()
    if command == "-print":
        command = input("Enter command: [-video, -keyWords, -categorie, -actor] ")
        if command == "-video":
            print(end="", flush=True)
            PrintVideoData()
        if command == "-keyWords":
            print(end="", flush=True)
            PrintKeyWordListList()
        if command == "-categorie":
            PrintCategorieAnalytics()
        if command == "-actor":
            PrintActorAnalytics()
    if command == "-help":
        print(end="", flush=True)
        print("This is the help page for gilltrickdb:\n You can enter these commands:\n --initdb: this initializes the database its like reloading\n --help: Prints this page")
        input("Press Enter to exit help")
        Run()
    if command == "-exit":
        exit()

def InitDB():
    LoadAnalyticalObjectList()
    LoadKeyWordListList()
    LoadCategorieAnalyticObjectList()
    LoadActorAnalyticObjectList()
    
def LoadAnalyticalObjectList():
    if os.path.exists(os.getcwd()+"/static/data/analytics/analytics.db"):
        global analyticalObjectList
        file = open(os.getcwd()+"/static/data/analytics/analytics.db", "rb")
        try:
            analyticalObjectList = pickle.load(file)
            print("ANALYTICS: AnalyticalObjectList loaded")
            file.close()
        except:
            print("ANALYTICS: Can't load analytics database")
            file.close()
    
def SaveAnalyticalObjectList():
    global analyticalObjectList
    file = open(os.getcwd()+"/static/data/analytics/analytics.db", "wb")
    pickle.dump(analyticalObjectList, file)
    file.close()

def LoadKeyWordListList():
    global keyWordListList
    if os.path.exists(os.getcwd()+"/static/data/analytics/keyWordList.db"):
        keyWordListListFile = open(os.getcwd()+"/static/data/analytics/keyWordList.db", "r").readlines()
        for line in keyWordListListFile:
            keyWordListList.append(re.split(",\s", line))
        print("ANALYTICS: Loaded keyWordList" )
        return
    print("ANALYTICS: Can't load keyWordList.db")

def SaveKeyWordList(_keyWordList):
    global keyWordListList
    keyWordListList.append(_keyWordList)
    #try to save file
    line = "";
    for keyWord in _keyWordList:
        if line != "":
            line += ", " + keyWord
        if line == "":
            line += keyWord
    try:
        keyWordFile = open(os.getcwd()+"/static/data/analytics/keyWordList.db", "a")
        keyWordFile.write(line+"\n")
        keyWordFile.close()
        print("ANALYTICS: keyWordList.db updated")
    except:
        print("ANALYTICS: Can't update keyWordList.db. probably not an issue")
      
def LoadCategorieAnalyticObjectList():
    global categorieAnalyticObjectList
    if os.path.exists(os.getcwd()+"/static/data/analytics/categorieAnalytics.db"):
        try:
            categorieAnalyticObjectListFile = open(os.getcwd() + "/static/data/analytics/categorieAnalytics.db", "rb")
            try:
                categorieAnalyticObjectList = pickle.load(categorieAnalyticObjectListFile)
                categorieAnalyticObjectListFile.close()
            except:
                print("ANALYTICS: No valid data in categorieAnalytics.db file")
        except:
            print("ANALYTICS: Can't load categorieAnalytics.db, does the file exist?")
            return
    print("ANALYTICS: categorieAnalytics.db loaded")

def SaveCategorieAnalyticObjectList():
    global categorieAnalyticObjectList
    if os.path.exists(os.getcwd()+"/static/data/analytics/categorieAnalytics.db"):
        categorieAnalyticObjectListFile = open(os.getcwd() + "/static/data/analytics/categorieAnalytics.db", "wb")
        pickle.dump(categorieAnalyticObjectList, categorieAnalyticObjectListFile)
        categorieAnalyticObjectListFile.close()
        print("ANALYTICS: categoryAnalytics database saved")

def LoadActorAnalyticObjectList():
    global actorAnalyticObjectList
    if os.path.exists(os.getcwd()+"/static/data/analytics/actorAnalytics.db"):
        try:
            actorAnalyticObjectListFile = open(os.getcwd() + "/static/data/analytics/actorAnalytics.db", "rb")
            try:
                actorAnalyticObjectList = pickle.load(actorAnalyticObjectListFile)
                actorAnalyticObjectListFile.close()
            except:
                print("ANALYTICS: No data valid data in actorAnalytics.db file")
        except:
            print("ANALYTICS: Can't load actorAnalytics.db, does the file exist?")
            return

    print("ANALYTICS: actorAnalytics.db loaded")        

def SaveActorAnalyticObjectList():
    global actorAnalyticObjectList
    if os.path.exists(os.getcwd()+"/static/data/analytics/actorAnalytics.db"):
        actorAnalyticObjectListFile = open(os.getcwd() + "/static/data/analytics/actorAnalytics.db", "wb")
        pickle.dump(actorAnalyticObjectList, actorAnalyticObjectListFile)
        actorAnalyticObjectListFile.close()
        print("ANALYTICS: actorAnalytics database saved")

def UpdateActorObject(_actorName):
    global actorAnalyticObjectList
    for actorAnalyticObject in actorAnalyticObjectList:
        if _actorName == actorAnalyticObject.name:
            actorAnalyticObject.counter += 1
            print(("ANALYTICS: categorieAnalyticsObject: " + actorAnalyticObject.name + " in categoryAnalytics database updated."))
            SaveActorAnalyticObjectList()

def UpdateCategoryObject(_categoryName):
    global categorieAnalyticObjectList
    for categorieAnalyticObject in categorieAnalyticObjectList:
        if _categoryName == categorieAnalyticObject.name:
            categorieAnalyticObject.counter += 1
            print(("ANALYTICS: categorieAnalyticsObject: " + categorieAnalyticObject.name + " in categoryAnalytics database updated."))
            SaveCategorieAnalyticObjectList()
            
def AnalyticalObjectExits(_url):
    global analyticalObjectList
    for analyticalObject in analyticalObjectList:
        if analyticalObject.metaInformationObject.videoUrl == _url:
            analyticalObject.watchCounter += 1
            SaveAnalyticalObjectList()
            #append data
            return
    NewAnalyticalObject(_url)
    
def NewAnalyticalObject(_url):
    newAnalyticalObject = modules.AnaltycisObject()
    metaInformationObject = database.GetMetaInfromationObjectByVideoUrl(_url)
    try:
        if metaInformationObject.videoUrl == "":
            print("ANALYTICS: No metaInformationObject from database loaded")
            return
        if metaInformationObject.videoUrl != "":
            newAnalyticalObject.metaInformationObject = metaInformationObject
            newAnalyticalObject.watchCounter = 1
            newAnalyticalObject.id = CreateRandomId()
            analyticalObjectList.append(newAnalyticalObject)
            database.LoadPopularActorList()
            database.LoadPopularCategoryList()
            SaveAnalyticalObjectList()
            return
    except:
            print("ANALYTICS: No metaInformationObject from database loaded")
            return        
            
def AnalyseKeyWords():
    global keyWordListList
    tempListList = keyWordListList.copy()
    _kwList = []
    for keyWordList in tempListList:
        for keyWord in keyWordList:
            if keyWord not in _kwList():
                _kwList.append(keyWord)

def PrintCategorieAnalytics():
    global categorieAnalyticObjectList
    command = input("Choose option:\n (1) print all categorie names\n (2) print data of categorie by name\n (3) print categorie names sorted by view count\n (4) search and print categorie data\n Enter number: ")
    if command == "1":
        for categorieAnalyticObject in categorieAnalyticObjectList:
            print("Categorie-Name: " + categorieAnalyticObject.name)
        PrintCategorieAnalytics()
    if command == "2":
        nameList = []
        alphabeticalSortedCategorieAnalyticObjectList = []
        for categorieAnalyticObject in categorieAnalyticObjectList: 
            nameList.append(categorieAnalyticObject.name)
        nameList.sort()
        for name in nameList:
            for categorieAnalyticObject in categorieAnalyticObjectList:
                if categorieAnalyticObject.name == name:
                    alphabeticalSortedCategorieAnalyticObjectList.append(categorieAnalyticObject)
        for categorieAnalyticObject in alphabeticalSortedCategorieAnalyticObjectList:
            print("Category-Name: " + categorieAnalyticObject.name + "\nView-Count: " + str(categorieAnalyticObject.counter)+"\n")
        PrintCategorieAnalytics()
    if command == "3":
        tempList = categorieAnalyticObjectList.copy()
        counterList = []
        sortedCategoryAnalyticObjectList = []
        for categorieAnalyticObject in tempList:
            counterList.append(categorieAnalyticObject.counter)
        counterList.sort()
        for counter in counterList:
            for categorieAnalyticObject in tempList:
                if categorieAnalyticObject.counter == counter:
                    sortedCategoryAnalyticObjectList.append(categorieAnalyticObject)
                    tempList.remove(categorieAnalyticObject)
        #by this i get the first value in the list with the smallest counter. its easier to read in print :D
        for obj in sortedCategoryAnalyticObjectList:
            print("Name: " + obj.name + "\nCounter: " + str(obj.counter) + "\n")
        PrintCategorieAnalytics()
    if command == "4":
        command = input("Enter category name: ")
        for categorieAnalyticObject in categorieAnalyticObjectList:
            if categorieAnalyticObject.name == command:
                print("Category-Name: " + categorieAnalyticObject.name + "\nView-Count: " + str(categorieAnalyticObject.counter))
                PrintCategorieAnalytics()
        print("ANALYTICS: Categorie name not found")
        PrintCategorieAnalytics()
    if command == "-return":
            Run()
    if command == "-exit":
        exit()

def PrintActorAnalytics():
    global actorAnalyticObjectList
    print(str(len(actorAnalyticObjectList)))
    command = input("Choose option:\n (1) print all actor names\n (2) print data of actor by name\n (3) print actor names sorted by view count\n (4) search and print actor by name\n Enter number: ")
    if command == "1":
        for actorAnalyticObject in actorAnalyticObjectList:
            print("Actor-Name: " + actorAnalyticObject.name)
        PrintActorAnalytics()
    if command == "2":
        nameList = []
        alphabeticalSortedActorAnalyticObjectList = []
        for actorAnalyticObject in actorAnalyticObjectList: 
            nameList.append(actorAnalyticObject.name)
        nameList.sort()
        for name in nameList:
            for actorAnalyticObject in actorAnalyticObjectList:
                if actorAnalyticObject.name == name:
                    alphabeticalSortedActorAnalyticObjectList.append(actorAnalyticObject)
        for actorAnalyticObject in alphabeticalSortedActorAnalyticObjectList:
            print("Category-Name: " + actorAnalyticObject.name + "\nView-Count: " + str(actorAnalyticObject.counter)+"\n")
        PrintActorAnalytics()
    if command == "3":
        tempList = actorAnalyticObjectList.copy()
        counterList = []
        sortedCategoryAnalyticObjectList = []
        for actorAnalyticObject in tempList:
            counterList.append(actorAnalyticObject.counter)
        counterList.sort()
        for counter in counterList:
            for actorAnalyticObject in tempList:
                if actorAnalyticObject.counter == counter:
                    sortedCategoryAnalyticObjectList.append(actorAnalyticObject)
                    tempList.remove(actorAnalyticObject)
        #by this i get the first value in the list with the smallest counter. its easier to read in print :D
        for obj in sortedCategoryAnalyticObjectList:
            print("Name: " + obj.name + "\nCounter: " + str(obj.counter) + "\n")
        PrintActorAnalytics()
    if command == "4":
        command = input("Enter category name: ")
        for actorAnalyticObject in actorAnalyticObjectList:
            if actorAnalyticObject.name == command:
                print("Category-Name: " + actorAnalyticObject.name + "\nView-Count: " + str(actorAnalyticObject.counter))
                PrintCategorieAnalytics()
        print("ANALYTICS: Categorie name not found")
        PrintCategorieAnalytics()
    if command == "-return":
            Run()
    if command == "-exit":
        exit()
            
def PrintVideoData():
    global analyticalObjectList
    for analyticalObject in analyticalObjectList:
        print("Video-Title: " + analyticalObject.metaInformationObject.videoTitle + "\nWatch-Counter: " + str(analyticalObject.watchCounter)+"\n")
    print("Records count: " + str(len(analyticalObjectList)))
        
def PrintKeyWordListList():
    global keyWordListList
    for keyWordList in keyWordListList:
        for keyWord in keyWordList:
            print("Keyword: " + keyWord)  

def CreateActorNameList():   
    file = open(os.getcwd()+"/static/data/dictionarys/categorieDictionary")
    lines = file.readlines()
    tempList = []
    for line in lines:
        line = re.sub("\n", "", line)
        tempList.append(line)
    return tempList

def LoadPopularCategorieList():
    global categorieAnalyticObjectList
    popularCategoriesList = []
    tempList = categorieAnalyticObjectList.copy()
    counterList = []
    sortedCategorieAnalyticObjectList = []
    for categorieAnalyticObject in tempList:
        counterList.append(categorieAnalyticObject.counter)
    counterList.sort()
    for counter in counterList:
        for categorieAnalyticObject in tempList:
            if categorieAnalyticObject.counter == counter:
                sortedCategorieAnalyticObjectList.append(categorieAnalyticObject)
                tempList.remove(categorieAnalyticObject)
    counter = 0
    for categorieAnalyticObject in sortedCategorieAnalyticObjectList:
        if counter < 32:
            popularCategoriesList.append(categorieAnalyticObject)
            couter += 1
    return popularCategoriesList

def LoadPopularActorList():
    global actorAnalyticObjectList
    popularActorsList = []
    tempList = actorAnalyticObjectList.copy()
    counterList = []
    sortedActorAnalyticObjectList = []
    for actorAnalyticObject in tempList:
        counterList.append(actorAnalyticObject.counter)
    counterList.sort()
    for counter in counterList:
        for actorAnalyticObject in tempList:
            if actorAnalyticObject.counter == counter:
                sortedActorAnalyticObjectList.append(actorAnalyticObject)
                tempList.remove(actorAnalyticObject)
    counter = 0
    for actorAnalyticObject in sortedActorAnalyticObjectList:
        if counter < 32:
            popularActorsList.append(actorAnalyticObject)
            couter += 1
    return popularActorsList
          
def CreateRandomId():
    return hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()


if __name__ == "__main__":
    Run()
