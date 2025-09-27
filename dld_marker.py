# Programmer : David Buddrige
# Purpose    : This program applies a series of tests on HTML files
#              using regular expressions to identify common errors
#              that would result in a student needing to fix and
#              resubmit their code.

import os
import sys
import re
from enum import Enum

directory_argument = '-dir'
ping_docs_argument = '-pingDocs'
web_development_argument = '-webdev'
required_parameter_list = [directory_argument]
optional_parameter_list = [ping_docs_argument,web_development_argument]
IMAGE_TOO_BIG = 307200
IMAGE_SIZE_WARNING = 60000

class MessageType(Enum):
    LABEL = "LABEL"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

def getRelativePathFromFullPath(fullPath):
    return str(fullPath).replace(paramDictionary[directory_argument],"")


def print_message(messageType: MessageType, message):    
    print(messageType.value + ",\"" + message.strip() + "\"")


def is_a_parameter(the_parameter):    
    retVal = False
    paramsToCheck = required_parameter_list + optional_parameter_list
    for p in paramsToCheck:
        if(the_parameter == p):
            retVal = True
    return retVal

def is_name_of_current_program(name_to_check):
    CURRENT_PROGRAM = os.path.basename(__file__)
    is_the_same = re.search(CURRENT_PROGRAM,name_to_check)
    return is_the_same

def parse_arguments():
    parameter_dictionary = { 
        ping_docs_argument: False,
        web_development_argument: False
    }
    next_parameter = None
    for parameter in sys.argv:
        if(is_name_of_current_program(parameter)):            
            print_message(MessageType.INFO, "Running " + parameter)
        else:
            if(is_a_parameter(parameter)):
                if(parameter == ping_docs_argument):
                    # the -pingDocs parameter is an on/off setting and takes no arguments
                    parameter_dictionary[parameter] = True
                    next_parameter = None
                elif(parameter == web_development_argument):
                    # the -webdev parameter is an on/off setting and takes no arguments
                    parameter_dictionary[parameter] = True
                    next_parameter = None
                else:
                    next_parameter = parameter
            elif(next_parameter != None):
                parameter_dictionary[next_parameter] = parameter
                next_parameter = None
            else:            
                message = "Parameter " + parameter + " is undefined"
                print(message)
    for parameter in required_parameter_list:
        if(not (parameter in parameter_dictionary)):            
            print("Parameter " + parameter + " is missing!")
            sys.exit()
    return parameter_dictionary

def is_valid_directory_or_file(directory_to_check):
    is_valid = True
    invalid_directories = ['__MACOSX$','.git$','.idea$','.gitignore$','.vscode$']
    for invalid_directory in invalid_directories:
        is_a_match = re.search(invalid_directory,directory_to_check)
        if(is_a_match):
            is_valid = False
    return is_valid
           

def findAllDirectories(dirToFind):    
    listOfDirs = []
    if(is_valid_directory_or_file(dirToFind)):
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
        if(is_valid_directory_or_file(fod)):
            subPath = dirToCheck + os.path.sep + fod
            if(os.path.isfile(subPath)):
                listOfFiles.append(subPath)
    return listOfFiles

def check_for_uppercase(folder_name):
    base_folder_name = os.path.basename(folder_name)
    if(base_folder_name.islower()==False):
        print_message(MessageType.ERROR,"UPPER CASE FOLDERNAME: The folder '" + getRelativePathFromFullPath( base_folder_name ) + "' includes upper case characters in violation of standards.  Please correct: " + getRelativePathFromFullPath(folder_name))
    else:
        print_message(MessageType.INFO,"Folder '" + base_folder_name  + "' is OK.")

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
                check_for_uppercase( dirToCheck + os.path.sep + fod)
                hasCss = True
            if(fod == 'js'):
                check_for_uppercase( dirToCheck + os.path.sep + fod)
                hasJs = True
            if(fod == 'img' or fod == 'images'):
                imgFolder = fod
                check_for_uppercase( dirToCheck + os.path.sep + fod)
                hasImages = True
            
    if(hasCss==False):
        print_message(MessageType.ERROR,"MISSING CSS DIRECTORY: Directory '" + getRelativePathFromFullPath(dirToCheck) + "' is missing a css folder in violation of standards")
    else:
        print_message(MessageType.INFO,"css folder found")
    if(hasJs==False):
        print_message(MessageType.ERROR,"MISSING JS DIRECTORY: Directory '" + getRelativePathFromFullPath(dirToCheck) + "' is missing a js folder in violation of standards")
    else:
        print_message(MessageType.INFO,"js folder found")
    if(hasImages==False):
        print_message(MessageType.ERROR,"MISSING IMAGES DIRECTORY: Directory '" + getRelativePathFromFullPath(dirToCheck) + "' is missing an images folder in violation of standards")
    else:
        print_message(MessageType.INFO,imgFolder + " folder found")
        imgDirsInWebsite = allDirs = findAllDirectories(dirToCheck + os.path.sep + imgFolder)
        for diw in imgDirsInWebsite:
            fid = findAllFiles(diw)               
            for imgFile in fid:
                checkIfImage(imgFile) 
               
        
    if(hasIndex==False):
        print_message(MessageType.ERROR,"MISSING INDEX.HTML: Directory '" + getRelativePathFromFullPath(dirToCheck) + "' is missing an index.html file in violation of standards")
    else:
        print_message(MessageType.INFO,"index.html found")
           
def testForSpan(htmlLine, lineNumber, htmlFile):
    # Check for <span>
    fileNameOnly = os.path.basename(htmlFile)
    hasSpan = re.search("<span", htmlLine, re.RegexFlag.IGNORECASE)
    if(hasSpan):
        print_message(MessageType.WARNING,fileNameOnly + "(" + str(lineNumber) +  "): <SPAN> LOCATED: <span> found on line "  + str(lineNumber) + " of file: '" + htmlFile + "' in violation of standards.")
        print_message(MessageType.WARNING,htmlLine)
   
def directoryContainsAHtmlFile(dirToCheck):
    hasAHtmlFile = False
    allFilesAndDirs = os.listdir(dirToCheck)
    for fod in allFilesAndDirs:
        if(os.path.isfile(dirToCheck + os.path.sep + fod)):
            if(re.search("html$",fod,re.RegexFlag.IGNORECASE)):
                # Then we have found at least one html file.  This directory is assumed to be a website, and will be checked accordingly."   
                print_message(MessageType.LABEL,"")             
                print_message(MessageType.LABEL,"===================================================================================================================")
                print_message(MessageType.LABEL,"Processing website directory: '" + dirToCheck + os.path.sep + fod + "'")
                print_message(MessageType.LABEL,"===================================================================================================================")
                      
                hasAHtmlFile = True
                break
    return hasAHtmlFile   

            
def testAHtmlFile(htmlFilePath, paramsDictionaryToUse):
    print_message(MessageType.INFO,"Testing html file '" + getRelativePathFromFullPath(htmlFilePath) + "'")
    fileNameOnly = os.path.basename(htmlFilePath)

    divCount = 0
    lineNumber = 0
    with open(htmlFilePath) as theHtmlFile:
        try:
            for textline in theHtmlFile:
                lineNumber += 1
                # Check for many <div> elements - but only if the -webdev flag isn't active. 
                # We allow multiple div's in web dev essentials class.
                if(paramsDictionaryToUse[web_development_argument]==False):
                    hasDiv = re.search("<div", textline, re.RegexFlag.IGNORECASE)
                    if(hasDiv):
                        divCount += 1
                        if(divCount > 1):
                            print_message(MessageType.ERROR,fileNameOnly + "(" + str(lineNumber) +  "): MULTIPLE <DIV> LOCATED: More than one <div> found on line " + str(lineNumber) + " of file: " + htmlFilePath + "' in violation of standards.  This is <div> number " + str(divCount) )
                            print_message(MessageType.ERROR,textline)
            
                # test for <span>    
                testForSpan(textline,lineNumber, htmlFilePath)
                    
                # test for <img> without alt property
                # Note that this will not register <img> tags where the tag has been broken over more than one line
                hasImg = re.search("<img\\s.+>", textline, re.RegexFlag.IGNORECASE)
                if(hasImg != None):                    
                    hasAlt = re.search("\\salt[\\s]*=",textline, re.RegexFlag.IGNORECASE)
                    if(hasAlt == None):
                        print_message(MessageType.ERROR,fileNameOnly + "(" + str(lineNumber) +  "): MISSING ALT: <img> missing alt on line "  + str(lineNumber) + " of file: " + getRelativePathFromFullPath(htmlFilePath))
                        print_message(MessageType.ERROR,textline)
                else:
                    hasImg = re.search("<img\\s", textline, re.RegexFlag.IGNORECASE)
                    if(hasImg != None):
                        hasAlt = re.search("\\salt[\\s]*=",textline, re.RegexFlag.IGNORECASE)
                        if(hasAlt == None):
                            print_message(MessageType.ERROR,fileNameOnly + "(" + str(lineNumber) +  "): POSSIBLE MISSING ALT - check next line of html: <img> missing alt on line "  + str(lineNumber) + " of file: " + getRelativePathFromFullPath(htmlFilePath))
                            print_message(MessageType.ERROR,textline)
                        hasHeight = re.search("\\sheight[\\s]*=",textline, re.RegexFlag.IGNORECASE)
                        if(hasHeight != None):
                            print_message(MessageType.ERROR,fileNameOnly + "(" + str(lineNumber) +  "): HEIGHT PROPERTY IN HTML- The height property should be specified in your css, not in your html."  + str(lineNumber) + " of file: " + htmlFilePath)
                            print_message(MessageType.ERROR,textline)
                        hasWidth = re.search("\\swidth[\\s]*=",textline, re.RegexFlag.IGNORECASE)
                        if(hasWidth != None):
                            print_message(MessageType.ERROR,fileNameOnly + "(" + str(lineNumber) +  "): WIDTH PROPERTY IN HTML- The width property should be specified in your css, not in your html."  + str(lineNumber) + " of file: " + getRelativePathFromFullPath(htmlFilePath))
                            print_message(MessageType.ERROR,textline)                
                # Check for uppercase tags
                hasUppercaseTag = re.search("<[A-Z]+",textline)
                if(hasUppercaseTag):
                    print_message(MessageType.ERROR,fileNameOnly + "(" + str(lineNumber) +  "): UPPER CASE HTML: found on line "  + str(lineNumber) + " of file: " + getRelativePathFromFullPath(htmlFilePath))
                    print_message(MessageType.ERROR,textline)
                
                # Check for other things at some point
        
        except Exception as ex:
            # template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            # message = template.format(type(ex).__name__, ex.args)
            print_message(MessageType.ERROR,"POSSIBLE FOREIGN UNICODE: Exception of type : " + str(type(ex).__name__ )) 
            print_message(MessageType.ERROR,"Error occurred on line " + str(lineNumber) + " of file: " + htmlFilePath)    
    
def isOneOfTheAcceptableNonStandardFiles(filePath):
    isOkNonStandard = False
    if(paramDictionary[ping_docs_argument]):
        isOkNonStandard = False
    else:    
        nonStandardFiles = ['.doc$','.docx$','.pdf$','.xls$','.xlsx$','.DS_Store$','.zip$']
        for nsf in nonStandardFiles:
            isOk = re.search(nsf,filePath,re.RegexFlag.IGNORECASE)  
            if(isOk):
                print_message(MessageType.INFO,"File: '" + getRelativePathFromFullPath(filePath) + "' is ignored.")
                isOkNonStandard = True
                break
    return isOkNonStandard
        
            
def checkFile(filePath):
    fileNameOnly = os.path.basename(filePath)
    if(isOneOfTheAcceptableNonStandardFiles(filePath) == False):
        if(fileNameOnly.islower()==False):
            print_message(MessageType.ERROR,"UPPER CASE FILENAME: '" + fileNameOnly + "'. The file '" + getRelativePathFromFullPath(filePath) + "' contains upper case characters in violation of standards")
        if(' ' in fileNameOnly):
            print_message(MessageType.ERROR,"SPACES IN FILENAME: '" + fileNameOnly + "'. The file '" + getRelativePathFromFullPath(filePath) + "' contains space characters in violation of standards")
    return fileNameOnly

    

def checkIfImage(imageFilename):
    isImage = re.search("jpg$|gif$|png$|svg$",imageFilename,re.RegexFlag.IGNORECASE)
    if(isImage != None):
        try:
            print_message(MessageType.INFO,"Check image file: " + getRelativePathFromFullPath(imageFilename))
        except:
            print_message(MessageType.WARNING,"error checking for image file")
            #printMessage(MessageType.INFO,"Check image file: " + imageFilename)
        fileSize = os.path.getsize(imageFilename)
        if(fileSize > IMAGE_TOO_BIG):
            print_message(MessageType.ERROR,"IMAGE TOO BIG: (" + str(fileSize) + " bytes). The file '" + getRelativePathFromFullPath(imageFilename) + "' has a filesize of " + str(fileSize) + ".  Images should be less than " + str(IMAGE_TOO_BIG) + " bytes.")
        else:
            if(fileSize > IMAGE_SIZE_WARNING):
                print_message(MessageType.WARNING,"IMAGE MIGHT BE TOO BIG: (" + str(fileSize) + " bytes). Most images should be less than " + str(IMAGE_SIZE_WARNING) + " bytes, unless they're a background image. The file '" + getRelativePathFromFullPath(imageFilename) + "' has a filesize of " + str(fileSize))
        # Check for capital letters or spaces in the filename.
        fileNameOnly = os.path.basename(imageFilename)
        hasUpperCaseFilename = re.search("[A-Z]+",fileNameOnly)
        if(hasUpperCaseFilename):
            print_message(MessageType.ERROR,"UPPER CASE filename: " + fileNameOnly  + " found at: " + getRelativePathFromFullPath(imageFilename)) 

if __name__ == "__main__":
    print("MessageCode, Message")
    paramDictionary = parse_arguments()

    if(os.path.exists(paramDictionary[directory_argument])):    
        print_message(MessageType.INFO,"Processing " + paramDictionary[directory_argument])
        allDirs = findAllDirectories(paramDictionary[directory_argument])    
        num_dirs_failed = 0
        num_dirs_processed = 0
        total_dirs = 0
        for d in allDirs:        
            total_dirs += 1
            try:
            
                if(directoryContainsAHtmlFile(d)):
                    hasRequiredDirsAndFiles(d)
                    filesInDir = findAllFiles(d)
                    for file_name in filesInDir:
                        try:                
                            isHtml = re.search("html$",file_name,re.RegexFlag.IGNORECASE)
                            if(isHtml):                    
                                testAHtmlFile(file_name,paramDictionary)
                        except:
                            print_message(MessageType.WARNING,"POSSIBLE FOREIGN UNICODE: Unable to print file from dir '" + d + "'.  This is most commonly caused by the use of non-english unicode character sets.")
                    print_message(MessageType.LABEL," -------------------------------------------- END OF WEBSITE PROCESSING -------------------------------------------")
                    print_message(MessageType.LABEL,"")
                    num_dirs_processed += 1
            except:
                num_dirs_failed += 1
                print("Unable to process: " + d)
        print("Processed",num_dirs_processed,"directories.", num_dirs_failed, "directories could not processed.")
    else:
        print("Directory " + paramDictionary[directory_argument] + " not found.")
        sys.exit()
