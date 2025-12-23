import re              # Import the regular expression library
import os              # Import operating system library
import sys             # Import system library
from enum import Enum  # Import Enumeration library

DIRECTORY_ARGUMENT = '-dir'
PING_DOCS_ARGUMENT = '-pingDocs'
WEB_DEVELOPMENT_ARGUMENT = '-webdev'
REQUIRED_PARAMETER_LIST = [DIRECTORY_ARGUMENT]
OPTIONAL_PARAMETER_LIST = [PING_DOCS_ARGUMENT,WEB_DEVELOPMENT_ARGUMENT]
IMAGE_TOO_BIG = 307200
IMAGE_SIZE_WARNING = 60000

class MessageType(Enum):
    LABEL = "LABEL"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

def get_name_of_current_program():
    return os.path.basename(__file__).strip()
    

def is_name_of_current_program(name_to_check):
    return name_to_check.strip() == get_name_of_current_program():



def is_a_parameter(the_parameter, required_parameter_list = REQUIRED_PARAMETER_LIST, optional_parameter_list = OPTIONAL_PARAMETER_LIST):    
    retVal = False
    paramsToCheck = required_parameter_list + optional_parameter_list
    for p in paramsToCheck:
        if(the_parameter == p):
            retVal = True
    return retVal

def parse_arguments():
    parameter_dictionary = { 
        PING_DOCS_ARGUMENT: False,
        WEB_DEVELOPMENT_ARGUMENT: False
    }
    next_parameter = None
    for parameter in sys.argv:
        if(not is_name_of_current_program(parameter)):            
            if(is_a_parameter(parameter)):
                if(parameter == PING_DOCS_ARGUMENT):
                    # the -pingDocs parameter is an on/off setting and takes no arguments
                    parameter_dictionary[parameter] = True
                    next_parameter = None
                elif(parameter == WEB_DEVELOPMENT_ARGUMENT):
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
    for parameter in REQUIRED_PARAMETER_LIST:
        if(not (parameter in parameter_dictionary)):            
            print("Parameter " + parameter + " is missing!")
            sys.exit()
    return parameter_dictionary


if __name__ == "__main__":
    message_list = []
    message_list.append(MessageType.INFO, "Running " + get_name_of_current_program())

    # print("MessageCode, Message")
    paramDictionary = parse_arguments()