import csv
import os
import time  
import datetime as dt
from operator import itemgetter     

def cleanupFileAge(age, path = '/log'):
    maxFileAge = age ## Days
    dirname = os.path.dirname(__file__) + path
    for filename in os.listdir(dirname):
        file = os.path.join(dirname, filename)
        # checking if it is a file
        if os.path.isfile(file):
            fileAge = time.time() - os.path.getmtime(file)
            if fileAge > (maxFileAge*86400):
                print("Deleting: ", file)
                os.remove(file)


def cleanupFilesize(size, path = '/log'):
    maxDirSize = size ## Mb
    fileList = []
    folderSize = 0
    dirname = os.path.dirname(__file__) + path
    for filename in os.listdir(dirname):
        file = os.path.join(dirname, filename)
        # checking if it is a file
        if os.path.isfile(file):
            fileAge = time.time() - os.path.getmtime(file)
            fileSize = os.path.getsize(file)
            folderSize += fileSize
            fileInfo = [file,fileAge, fileSize]
            fileList.append(fileInfo)
    fileList = sorted(fileList,key=itemgetter(1),reverse = True)
    print(folderSize)
    if folderSize > maxDirSize:
        tempFolderSize = folderSize
        counter = 0
        while tempFolderSize > (maxDirSize*0.9):
            print(fileList[counter][0], fileList[counter][2])
            os.remove(fileList[counter][0])
            tempFolderSize -= fileList[counter][2]
            counter += 1
            print(tempFolderSize)

def logToCSV(data, path = 'log/', suffix = '_sun2000.csv'):
    dirname = os.path.dirname(__file__)
    fileName = path + str(dt.datetime.now().strftime("%Y-%m-%d")) + suffix
    filePath = os.path.join(dirname, fileName)
    with open(filePath, mode='a') as logfile:
        employee_writer = csv.writer(logfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(data)

