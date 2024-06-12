# Programmer : David Buddrige
# Purpose    : This program applies a series of tests on HTML files
#              using regular expressions to identify common errors
#              that would result in a student needing to fix and
#              resubmit their code.

import os
import sys
import re

dirArg = '-dir'
pingDocsArg = '-pingDocs'
requiredParamArray = [dirArg]
optionalParmArray = [pingDocsArg]

def isAParam(theParam):    
    retVal = False
    paramsToCheck = requiredParamArray + optionalParmArray
    #print("Checking " + str(paramsToCheck))
    for p in paramsToCheck:
        if(theParam == p):
            retVal = True
    return retVal

def parseArgs():
    paramDict = { 
        pingDocsArg: False
    }
    #print(paramDict)
    nextP = None
    #print(sys.argv)
    for p in sys.argv:
        isMainProgram = re.search("html-tester.py",p)
        if(isMainProgram):            
            print("Running " + p)
        else:
            #print("Loading " + p)
            if(isAParam(p)):
                nextP = p
                if(p == pingDocsArg):
                    # the -pingDocs parameter is an on/off setting and takes no arguments
                    paramDict[p] = True
                    nextP = None
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
            #print("Matched " + inv + " with " + dirToCheck)
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
        print("UPPER CASE FOLDERNAME: The folder \"" + folderName + "\" includes upper case characters in violation of standards")

def hasRequiredDirsAndFiles(dirToCheck):
    hasCss = False
    hasImages = False
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
                checkForUpper( dirToCheck + os.path.sep + fod)
                hasImages = True
            
    if(hasCss==False):
        print("MISSING CSS DIRECTORY: Directory \"" + dirToCheck + "\" is missing a css folder in violation of standards")
    if(hasJs==False):
        print("MISSING JS DIRECTORY: Directory \"" + dirToCheck + "\" is missing a js folder in violation of standards")
    if(hasImages==False):
        print("MISSING IMAGES DIRECTORY: Directory \"" + dirToCheck + "\" is missing an images folder in violation of standards")
    if(hasIndex==False):
        print("MISSING INDEX.HTML: Directory \"" + dirToCheck + "\" is missing an index.html file in violation of standards")
           
def testForSpan(htmlLine, lineNumber, htmlFile):
    # Check for <span>
    hasSpan = re.search("<span", htmlLine, re.RegexFlag.IGNORECASE)
    if(hasSpan):
        print("<SPAN> LOCATED: <span> found on line "  + str(lineNumber) + " of file: \"" + htmlFile + "\" in violation of standards.")
        print(htmlLine)
   
def directoryContainsAHtmlFile(dirToCheck):
    hasAHtmlFile = False
    allFilesAndDirs = os.listdir(dirToCheck)
    for fod in allFilesAndDirs:
        if(os.path.isfile(dirToCheck + os.path.sep + fod)):
            if(re.search("html$",fod,re.RegexFlag.IGNORECASE)):
                # Then we have found at least one html file.  This directory is assumed to be a website, and will be checked accordingly."   
                print("")             
                print("===================================================================================================================")
                print("Processing website directory: \"" + dirToCheck + os.path.sep + fod + "\"")
                print("===================================================================================================================")
                      
                hasAHtmlFile = True
                break
    return hasAHtmlFile   

            
def testAHtmlFile(htmlFilePath):
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
                        print("MULTIPLE <DIV> LOCATED: More than one <div> found on line " + str(lineNumber) + " of file: " + htmlFilePath + "\" in violation of standards.  This is <div> number " + str(divCount) )
                        print(textline)
                
                # test for <span>    
                testForSpan(textline,lineNumber, htmlFilePath)
                    
                # test for <img> without alt property
                # Note that this will not register <img> tags where the tag has been broken over more than one line
                hasImg = re.search("<img\\s.+>", textline, re.RegexFlag.IGNORECASE)
                if(hasImg != None):                    
                    hasAlt = re.search("\\salt[\\s]*=",textline, re.RegexFlag.IGNORECASE)
                    if(hasAlt == None):
                        print("MISSING ALT: <img> missing alt on line "  + str(lineNumber) + " of file: " + htmlFilePath)
                        print(textline)
                else:
                    hasImg = re.search("<img\\s", textline, re.RegexFlag.IGNORECASE)
                    if(hasImg != None):
                        hasAlt = re.search("\\salt[\\s]*=",textline, re.RegexFlag.IGNORECASE)
                        if(hasAlt == None):
                            print("POSSIBLE MISSING ALT - check next line of html: <img> missing alt on line "  + str(lineNumber) + " of file: " + htmlFilePath)
                            print(textline)
                    
                            
                # Check for uppercase tags
                hasUppercaseTag = re.search("<[A-Z]+",textline)
                if(hasUppercaseTag):
                    print("UPPER CASE HTML: found on line "  + str(lineNumber) + " of file: " + htmlFilePath)
                    print(textline)
                        
                # Check for 
        
        except Exception as ex:
            # template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            # message = template.format(type(ex).__name__, ex.args)
            print("POSSIBLE FOREIGN UNICODE: Exception of type : " + str(type(ex).__name__ )) 
            print("Error occurred on line " + str(lineNumber) + " of file: " + htmlFilePath)    
    
def isOneOfTheAcceptableNonStandardFiles(filePath):
    isOkNonStandard = False
    if(paramDictionary[pingDocsArg]):
        isOkNonStandard = False
    else:    
        nonStandardFiles = ['.doc$','.docx$','.pdf$','.xls$','.xlsx$','.DS_Store$','.zip$']
        for nsf in nonStandardFiles:
            isOk = re.search(nsf,filePath,re.RegexFlag.IGNORECASE)  
            if(isOk):
                isOkNonStandard = True
                break
    return isOkNonStandard
        
            
def checkFile(filePath):
    fileNameOnly = os.path.basename(filePath)
    if(isOneOfTheAcceptableNonStandardFiles(filePath) == False):
        if(fileNameOnly.islower()==False):
            print("UPPER CASE FILENAME: The file \"" + filePath + "\" contains upper case characters in violation of standards")
        if(' ' in fileNameOnly):
            print("SPACES IN FILENAME: The file \"" + filePath + "\" contains space characters in violation of standards")
    return fileNameOnly

paramDictionary = parseArgs()

if(os.path.exists(paramDictionary[dirArg])):    
    print("Processing " + paramDictionary[dirArg])
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
                    print("POSSIBLE FOREIGN UNICODE: Unable to print file from dir \"" + d + "\".  This is most commonly caused by the use of non-english unicode character sets.")
            print(" -------------------------------------------- END OF WEBSITE PROCESSING -------------------------------------------")
            print("")
else:
    print("Directory " + paramDictionary[dirArg] + " not found.")
    sys.exit()
