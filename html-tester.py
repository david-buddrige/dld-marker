# Programmer : David Buddrige
# Purpose    : This program applies a series of tests on HTML files
#              using regular expressions to identify common errors
#              that would result in a student needing to fix and
#              resubmit their code.

import os
import sys
import re
from enum import Enum

dirArg = '-dir'
pingDocsArg = '-pingDocs'
requiredParamArray = [dirArg]
optionalParmArray = [pingDocsArg]

class MessageType(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

def printMessage(messageType: MessageType, message):
    
    print(messageType.value + ",\"" + message.strip() + "\"")


def isAParam(theParam):    
    retVal = False
    paramsToCheck = requiredParamArray + optionalParmArray
    for p in paramsToCheck:
        if(theParam == p):
            retVal = True
    return retVal

def parseArgs():
    paramDict = { 
        pingDocsArg: False
    }
    nextP = None
    for p in sys.argv:
        isMainProgram = re.search("html-tester.py",p)
        if(isMainProgram):            
            printMessage(MessageType.INFO, "Running " + p)
        else:
            if(isAParam(p)):
                if(p == pingDocsArg):
                    # the -pingDocs parameter is an on/off setting and takes no arguments
                    paramDict[p] = True
                    nextP = None
                else:
                    nextP = p
            elif(nextP != None):
                paramDict[nextP] = p
                nextP = None
            else:            
                message = "Parameter " + p + " is undefined"
                print(message)
    for p in requiredParamArray:
        if(not (p in paramDict)):            
            print("Parameter " + p + " is missing!")
            sys.exit()
    return paramDict

def isValidDirOrFile(dirToCheck):
    isValid = True
    invalidDirs = ['__MACOSX$','.git$','.idea$','.gitignore$','.vscode$']
    for inv in invalidDirs:
        isaMatch = re.search(inv,dirToCheck)
        if(isaMatch):
            isValid = False
    return isValid
           

def findAllDirectories(dirToFind):    
    listOfDirs = []
    if(isValidDirOrFile(dirToFind)):
        listOfDirs = [dirToFind]    
        allFilesAndDirs = os.listdir(dirToFind)
        for fod in allFilesAndDirs:
            subPath = dirToFind + os.path.sep + fod
            if(os.path.isdir(subPath)):            
                subList = findAllDirectories(subPath)
                listOfDirs = listOfDirs + subList
    return listOfDirs


def findAllFiles(dirToCheck):
    listOfFiles = []
    allFilesAndDirs = os.listdir(dirToCheck)
    for fod in allFilesAndDirs:
        if(isValidDirOrFile(fod)):
            subPath = dirToCheck + os.path.sep + fod
            if(os.path.isfile(subPath)):
                listOfFiles.append(subPath)
    return listOfFiles

def checkForUpper(folderName):
    fod = os.path.basename(folderName)
    if(fod.islower()==False):
        printMessage(MessageType.ERROR,"UPPER CASE FOLDERNAME: The folder '" + folderName + "' includes upper case characters in violation of standards")
    else:
        printMessage(MessageType.INFO,"Folder '" + folderName + "' is OK")

def hasRequiredDirsAndFiles(dirToCheck):
    hasCss = False
    hasImages = False
    imgFolder = ""
    hasJs = False
    hasIndex = False
    allFilesAndDirs = os.listdir(dirToCheck)
    for fod in allFilesAndDirs:
        if(os.path.isfile(dirToCheck + os.path.sep + fod)):
            checkFile(dirToCheck + os.path.sep + fod)
            if(fod=='index.html'):
                hasIndex = True
        else:          
            if(re.match('css$',fod,re.RegexFlag.IGNORECASE)):
                checkForUpper( dirToCheck + os.path.sep + fod)
                hasCss = True
            if(fod == 'js'):
                checkForUpper( dirToCheck + os.path.sep + fod)
                hasJs = True
            if(fod == 'img' or fod == 'images'):
                imgFolder = fod
                checkForUpper( dirToCheck + os.path.sep + fod)
                hasImages = True
            
    if(hasCss==False):
        printMessage(MessageType.ERROR,"MISSING CSS DIRECTORY: Directory '" + dirToCheck + "' is missing a css folder in violation of standards")
    else:
        printMessage(MessageType.INFO,"css folder found")
    if(hasJs==False):
        printMessage(MessageType.ERROR,"MISSING JS DIRECTORY: Directory '" + dirToCheck + "' is missing a js folder in violation of standards")
    else:
        printMessage(MessageType.INFO,"js folder found")
    if(hasImages==False):
        printMessage(MessageType.ERROR,"MISSING IMAGES DIRECTORY: Directory '" + dirToCheck + "' is missing an images folder in violation of standards")
    else:
        printMessage(MessageType.INFO,imgFolder + " folder found")
        imgDirsInWebsite = allDirs = findAllDirectories(dirToCheck + os.path.sep + imgFolder)
        for diw in imgDirsInWebsite:
            fid = findAllFiles(diw)               
            for imgFile in fid:
                checkIfImage(imgFile) 
               
        
    if(hasIndex==False):
        printMessage(MessageType.ERROR,"MISSING INDEX.HTML: Directory '" + dirToCheck + "' is missing an index.html file in violation of standards")
    else:
        printMessage(MessageType.INFO,"index.html found")
           
def testForSpan(htmlLine, lineNumber, htmlFile):
    # Check for <span>
    hasSpan = re.search("<span", htmlLine, re.RegexFlag.IGNORECASE)
    if(hasSpan):
        printMessage(MessageType.ERROR,"<SPAN> LOCATED: <span> found on line "  + str(lineNumber) + " of file: '" + htmlFile + "' in violation of standards.")
        printMessage(MessageType.ERROR,htmlLine)
   
def directoryContainsAHtmlFile(dirToCheck):
    hasAHtmlFile = False
    allFilesAndDirs = os.listdir(dirToCheck)
    for fod in allFilesAndDirs:
        if(os.path.isfile(dirToCheck + os.path.sep + fod)):
            if(re.search("html$",fod,re.RegexFlag.IGNORECASE)):
                # Then we have found at least one html file.  This directory is assumed to be a website, and will be checked accordingly."   
                printMessage(MessageType.INFO,"")             
                printMessage(MessageType.INFO,"===================================================================================================================")
                printMessage(MessageType.INFO,"Processing website directory: '" + dirToCheck + os.path.sep + fod + "'")
                printMessage(MessageType.INFO,"===================================================================================================================")
                      
                hasAHtmlFile = True
                break
    return hasAHtmlFile   

            
def testAHtmlFile(htmlFilePath):
    printMessage(MessageType.INFO,"Testing html file '" + htmlFilePath + "'")
    divCount = 0
    lineNumber = 0
    with open(htmlFilePath) as theHtmlFile:
        try:
            for textline in theHtmlFile:
                lineNumber += 1
                # Check for many <div> elements
                hasDiv = re.search("<div", textline, re.RegexFlag.IGNORECASE)
                if(hasDiv):
                    divCount += 1
                    if(divCount > 1):
                        printMessage(MessageType.ERROR,"MULTIPLE <DIV> LOCATED: More than one <div> found on line " + str(lineNumber) + " of file: " + htmlFilePath + "' in violation of standards.  This is <div> number " + str(divCount) )
                        printMessage(MessageType.ERROR,textline)
            
                # test for <span>    
                testForSpan(textline,lineNumber, htmlFilePath)
                    
                # test for <img> without alt property
                # Note that this will not register <img> tags where the tag has been broken over more than one line
                hasImg = re.search("<img\\s.+>", textline, re.RegexFlag.IGNORECASE)
                if(hasImg != None):                    
                    hasAlt = re.search("\\salt[\\s]*=",textline, re.RegexFlag.IGNORECASE)
                    if(hasAlt == None):
                        printMessage(MessageType.ERROR,"MISSING ALT: <img> missing alt on line "  + str(lineNumber) + " of file: " + htmlFilePath)
                        printMessage(MessageType.ERROR,textline)
                else:
                    hasImg = re.search("<img\\s", textline, re.RegexFlag.IGNORECASE)
                    if(hasImg != None):
                        hasAlt = re.search("\\salt[\\s]*=",textline, re.RegexFlag.IGNORECASE)
                        if(hasAlt == None):
                            printMessage(MessageType.ERROR,"POSSIBLE MISSING ALT - check next line of html: <img> missing alt on line "  + str(lineNumber) + " of file: " + htmlFilePath)
                            printMessage(MessageType.ERROR,textline)
                
                # Check for uppercase tags
                hasUppercaseTag = re.search("<[A-Z]+",textline)
                if(hasUppercaseTag):
                    printMessage(MessageType.ERROR,"UPPER CASE HTML: found on line "  + str(lineNumber) + " of file: " + htmlFilePath)
                    printMessage(MessageType.ERROR,textline)
                
                # Check for 
        
        except Exception as ex:
            # template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            # message = template.format(type(ex).__name__, ex.args)
            printMessage(MessageType.ERROR,"POSSIBLE FOREIGN UNICODE: Exception of type : " + str(type(ex).__name__ )) 
            printMessage(MessageType.ERROR,"Error occurred on line " + str(lineNumber) + " of file: " + htmlFilePath)    
    
def isOneOfTheAcceptableNonStandardFiles(filePath):
    isOkNonStandard = False
    if(paramDictionary[pingDocsArg]):
        isOkNonStandard = False
    else:    
        nonStandardFiles = ['.doc$','.docx$','.pdf$','.xls$','.xlsx$','.DS_Store$','.zip$']
        for nsf in nonStandardFiles:
            isOk = re.search(nsf,filePath,re.RegexFlag.IGNORECASE)  
            if(isOk):
                printMessage(MessageType.INFO,"File: '" + filePath + "' is ignored.")
                isOkNonStandard = True
                break
    return isOkNonStandard
        
            
def checkFile(filePath):
    fileNameOnly = os.path.basename(filePath)
    if(isOneOfTheAcceptableNonStandardFiles(filePath) == False):
        if(fileNameOnly.islower()==False):
            printMessage(MessageType.ERROR,"UPPER CASE FILENAME: The file '" + filePath + "' contains upper case characters in violation of standards")
        if(' ' in fileNameOnly):
            printMessage(MessageType.ERROR,"SPACES IN FILENAME: The file '" + filePath + "' contains space characters in violation of standards")
    return fileNameOnly

def checkIfImage(imageFilename):
    isImage = re.search("jpg$|gif$|png$|svg$",imageFilename,re.RegexFlag.IGNORECASE)
    if(isImage != None):
        printMessage(MessageType.INFO,"Check image file: " + imageFilename)
        fileSize = os.path.getsize(imageFilename)
        if(fileSize > 307200):
            printMessage(MessageType.ERROR,"IMAGE TOO BIG: The file '" + imageFilename + "' has a filesize of " + str(fileSize))
        else:
            if(fileSize > 60000):
                printMessage(MessageType.WARNING,"WARNING - IMAGE MIGHT BE TOO BIG: Most images should be less than 60 kilobytes, unless they're a background image. The file '" + imageFilename + "' has a filesize of " + str(fileSize))

paramDictionary = parseArgs()

if(os.path.exists(paramDictionary[dirArg])):    
    printMessage(MessageType.INFO,"Processing " + paramDictionary[dirArg])
    allDirs = findAllDirectories(paramDictionary[dirArg])    
    for d in allDirs:        
        if(directoryContainsAHtmlFile(d)):
            hasRequiredDirsAndFiles(d)
            filesInDir = findAllFiles(d)
            for f in filesInDir:
                try:                
                    isHtml = re.search("html$",f,re.RegexFlag.IGNORECASE)
                    if(isHtml):                    
                        testAHtmlFile(f)
                except:
                    printMessage(MessageType.WARNING,"POSSIBLE FOREIGN UNICODE: Unable to print file from dir '" + d + "'.  This is most commonly caused by the use of non-english unicode character sets.")
            printMessage(MessageType.INFO," -------------------------------------------- END OF WEBSITE PROCESSING -------------------------------------------")
            printMessage(MessageType.INFO,"")
else:
    print("Directory " + paramDictionary[dirArg] + " not found.")
    sys.exit()
