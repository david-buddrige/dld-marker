#from dld_marker import *
import os
import re
import sys
from enum import Enum


html_file_parameter = "-html-file-path"
required_parameter_list = [html_file_parameter]
the_optional_parameters = []

class MessageType(Enum):
    LABEL = "LABEL"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    
def check_parameter_in_list(the_parameter, required_parameter_list, optional_parameter_list):
    retVal = False
    parameters_to_check = required_parameter_list + optional_parameter_list
    for parameter in parameters_to_check:
        if(the_parameter == parameter):
            retVal = True
    return retVal

def is_name_of_current_program(name_to_check):
    CURRENT_PROGRAM = os.path.basename(__file__)
    is_the_same = re.search(CURRENT_PROGRAM,name_to_check)
    return is_the_same

def print_message(messageType: MessageType, message):    
    print(messageType.value + ",\"" + message.strip() + "\"")


def parse_arguments(required_parameter_list, the_optional_parameters):
    parameter_dictionary = { 
        # ping_docs_argument: False,
        # web_development_argument: False
    }
    next_parameter = None
    for parameter in sys.argv:
        if(is_name_of_current_program(parameter)):            
            print_message(MessageType.INFO, "Running " + parameter)
        else:
            if check_parameter_in_list(parameter, required_parameter_list, the_optional_parameters):
                next_parameter = parameter
            elif next_parameter != None:
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

def get_parameter_dictionary(required_parameter_list, the_optional_parameters):
    parameter_dictionary = parse_arguments(required_parameter_list, the_optional_parameters)

    return parameter_dictionary


def find_heading(heading, line):
    """
    Looks for a particular heading text in a line.
    
    For this function to return true, the string in heading must be found in line, 
    but the heading must be surrounded by a heading tag such as  <h1>, <h2>, <h3>
    etc.

    Args:
        heading (string): The heading that we're looking for.  It should be a 
        particular heading that we need to find, such as "Toy Breaking News"        
        line (string): The line from the web file that may or may-not have that heading

    Returns:
        Boolean: True if the heading is found in line and is wrapped in a html heading tag. 
    """
    if heading.lower() in line.lower():
        # then we know that the heading is in there somewhere. We just now need to find out
        # whether or not it is 
        heading_regex = "<[hH]\\d\\s*.*\\>" + heading + "\\<\\/h\\d\\>"
        
        result = re.search(heading_regex, line)
        if(result):
            # print  ("Found heading '" + heading + "'" )
            return True
        else:
            # print  ("heading '",heading, "' not found" )
            return False
        return True
    else:
        return False

def look_for_headings(headings, list_of_lines):
    
    
    found_dictionary = {}
    
    for heading in headings:
        found_dictionary[heading] = False
    
    for heading in headings:
        for line in list_of_lines:
            # print("Finding",heading,"in",line)

            if find_heading(heading, line):
                # print("Found",heading,"in",line)
                found_dictionary[heading] = True
    return found_dictionary
                

def get_list_of_strings_from_filename(filename):
    file_handle = open(filename,"r")
    list_of_lines = []
    for line in file_handle:
        list_of_lines.append(line.strip())
    file_handle.close()
    return list_of_lines
    

headings = ('Toy Pictures', 'Toy Prices', 'Toy Options', 'Toy News Article', 'Toy Breaking News')


def print_heading_check_result(headings_dictionary):
    print("\n")
    
    for heading, found in headings_dictionary.items():
        if found:
            print("Found '" + heading + "'")
        else:
            print("Missing '" + heading + "'")
            


if __name__ == "__main__":
    # print("Running program")
    # print("Heading finder")
    parameter_dictionary = get_parameter_dictionary(required_parameter_list, the_optional_parameters)
    
    if os.path.exists(parameter_dictionary[html_file_parameter]):
        # print(parameter_dictionary[html_file_parameter], "found") 
        lines_in_html_file = get_list_of_strings_from_filename(parameter_dictionary[html_file_parameter])
        found_dictionary = look_for_headings(headings, lines_in_html_file)
        print_heading_check_result(found_dictionary)
    else:
        print(parameter_dictionary[html_file_parameter], "not found")    
  
else:
    print("Running tests")