import re              # Import the regular expression library
import os              # Import operating system library
import sys             # Import system library
from enum import Enum  # Import Enumeration library

IGNORE_FILE_OR_DIRECTORY = ['__MACOSX$','.git$','.idea$','.gitignore$','.vscode$']
DIRECTORY_ARGUMENT = '-dir'
PING_DOCS_ARGUMENT = '-pingDocs'
WEB_DEVELOPMENT_ARGUMENT = '-webdev'
REQUIRED_PARAMETER_LIST = [DIRECTORY_ARGUMENT]
BOOLEAN_PARAMETER_LIST = [PING_DOCS_ARGUMENT,WEB_DEVELOPMENT_ARGUMENT]
IMAGE_TOO_BIG = 307200
IMAGE_SIZE_WARNING = 60000

class MessageType(Enum):
    LABEL = "LABEL"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

class Message:
    def __init__(self, message_type, message):
        self.message_type = message_type
        self.message = message

def get_name_of_current_program():
    return os.path.basename(__file__).strip()

def is_name_of_current_program(name_to_check):
    return name_to_check.strip() == get_name_of_current_program()

def is_a_parameter(the_parameter, required_parameter_list = REQUIRED_PARAMETER_LIST, optional_parameter_list = BOOLEAN_PARAMETER_LIST):    
    paramsToCheck = required_parameter_list + optional_parameter_list
    return the_parameter in paramsToCheck


def parse_arguments(required_parameter_list = REQUIRED_PARAMETER_LIST, boolean_parameter_list = BOOLEAN_PARAMETER_LIST):
    parameter_dictionary = { 
        PING_DOCS_ARGUMENT: False,
        WEB_DEVELOPMENT_ARGUMENT: False
    }
    
    next_parameter = None
    for parameter in sys.argv:
        if(not is_name_of_current_program(parameter)):            
            if(is_a_parameter(parameter)):
                
                if parameter in boolean_parameter_list:
                    # the -pingDocs parameter and the -webdev parameter is an on/off setting and takes no arguments
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
    # Check that we have the needed parameters
    for parameter in required_parameter_list:
        if not parameter in parameter_dictionary:            
            print("Parameter " + parameter + " is missing!")
            sys.exit()
    return parameter_dictionary

def is_valid_directory_or_file(file_or_directory_to_check, ignore_file_or_directory_list = IGNORE_FILE_OR_DIRECTORY):
    is_valid = True
    for invalid_directory in ignore_file_or_directory_list:
        is_a_match = re.search(invalid_directory, file_or_directory_to_check)
        if(is_a_match):
            is_valid = False
    return is_valid


def find_all_directories(directory_path_to_find):    
    list_of_directories = []
    if(is_valid_directory_or_file(directory_path_to_find)):
        list_of_directories = [directory_path_to_find]    
        all_directories = os.listdir(directory_path_to_find)
        for file_or_directory in all_directories:
            sub_path = directory_path_to_find + os.path.sep + file_or_directory
            if(os.path.isdir(sub_path)):            
                subList = find_all_directories(sub_path)
                list_of_directories = list_of_directories + subList
    return list_of_directories

if __name__ == "__main__":
    message_list = []
    
    process_message = Message(MessageType.INFO, "Running " + get_name_of_current_program()) 
    message_list.append(process_message)

    # print("MessageCode, Message")
    parameter_dictionary = parse_arguments()
    
    if(os.path.exists(parameter_dictionary[DIRECTORY_ARGUMENT])):    
        process_message = Message(MessageType.INFO,"Processing " + parameter_dictionary[DIRECTORY_ARGUMENT])
        message_list.append(process_message)
        all_directories = find_all_directories(parameter_dictionary[DIRECTORY_ARGUMENT])    
