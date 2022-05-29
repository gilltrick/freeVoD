import subprocess, os, re

sourceFolder = os.getcwd()+"/input/"
resultFolder = os.getcwd()+"/output"
sourceFileNameList = os.listdir(sourceFolder)
sourceFilePathList = []
resultFilePathList = []
counter = 0

for sourceFileName in sourceFileNameList:
    sourceFilePathList.append(sourceFolder+"/"+sourceFileName)
    resultFilePathList.append(resultFolder+"/"+re.sub(re.search("(\.\w+)", sourceFileName).group(1), ".mp4", sourceFileName))
    
for sourceFilePath in sourceFilePathList:
    print(sourceFilePath)
    print(resultFilePathList[counter])
    #ffmpeg -i input.avi -y output.mp4
    subprocess.call(['G:/dbz-converter/ffmpeg/bin/ffmpeg.exe', '-i', sourceFilePath, '-y', resultFilePathList[counter]])
    counter += 1
