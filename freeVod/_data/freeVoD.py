import os

def Run():
    command = input("Enter Command for freeVoD [-start, -database, -analytics, -userDatabase, -converter]: ")
    if command == "-start":
        os.system('python server.py')
    if command == "-converter":
        if os.path.exists(os.getcwd()+"/ffmpeg/ffmpeg.exe"):
            print("Starting Converter")
            os.system('python converter.py')
        else:
            print("You have to download and install the version with the converter included to use it")
    if command == "-database":
        print("Accessing database")
        os.system('python database.py')        
    if command == "-analytics":
        print("Accessing analytics database")
        os.system('python analytics.py')
    if command == "-userDatabase":
        print("Accessing user database")
        os.system('python userDatabase.py')
        
if __name__ == "__main__":
    Run()