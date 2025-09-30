# Programmer : David BUddrige
# Date       : 27 September, 2025
# Purpose    : To see if all headings required for DLD AT2 are in the code
# Usage      : python heading_finder.py -html-file "C:\path\filename.html"


import os
import re
import sys
from enum import Enum

HEADINGS = ('Toy Pictures', 'Toy Prices', 'Toy Options', 'Toy News Article', 'Toy Breaking News')

HTML_FILE_PARAMETER     = "-html-file"
REQUIRED_PARAMETER_LIST = [HTML_FILE_PARAMETER]
OPTIONAL_PARAMETER_LIST = []

HEADING_FOUND_KEY = "heading_found"
LINE_NUMBER_KEY   = "line_number",
LINE_KEY          = "line"
  
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

def parse_arguments(required_parameter_list, the_optional_parameters):
    parameter_dictionary = { }
    next_parameter = None
    for parameter in sys.argv:
        if(not is_name_of_current_program(parameter)):             
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
            return True
        else:
            return False
        return True
    else:
        return False
    
 
def get_heading_information(found, line_number, line):
    heading_information = {
        HEADING_FOUND_KEY : found,
        LINE_NUMBER_KEY   : line_number,
        LINE_KEY          : line
    } 
    return heading_information 


def look_for_headings(headings, list_of_lines):
    found_dictionary = {}
    
    for heading in headings:
        found_dictionary[heading] = get_heading_information(False, 0, "")
    
    for heading in headings:
        line_number = 1
        for line in list_of_lines:
            if find_heading(heading, line):
                found_dictionary[heading] = get_heading_information(True, line_number, line)
            line_number += 1
    return found_dictionary
                

def get_list_of_strings_from_filename(filename):
    list_of_lines = []     
    try:
        with open(filename,"r") as file_handle:
            for line in file_handle:
                list_of_lines.append(line.strip())
    except:
        print("Error processing",filename)
    return list_of_lines
    

def print_heading_check_result(html_file, headings, headings_dictionary):
    print("\n")
    print("Checked for headings: ", headings, "in", html_file)
    for heading, information in headings_dictionary.items():
        if information[HEADING_FOUND_KEY]:
            found_message = "Found '" + heading + "'" 
            print(found_message.ljust(30) + "Line:", information[LINE_NUMBER_KEY], ":", information[LINE_KEY])
        else:
            print("Missing '" + heading + "'")

            


if __name__ == "__main__":
    parameter_dictionary = get_parameter_dictionary(REQUIRED_PARAMETER_LIST, OPTIONAL_PARAMETER_LIST)
    
    if os.path.exists(parameter_dictionary[HTML_FILE_PARAMETER]):
        lines_in_html_file = get_list_of_strings_from_filename(parameter_dictionary[HTML_FILE_PARAMETER])
        found_dictionary = look_for_headings(HEADINGS, lines_in_html_file)
        print_heading_check_result(parameter_dictionary[HTML_FILE_PARAMETER], HEADINGS, found_dictionary)
    else:
        print(parameter_dictionary[HTML_FILE_PARAMETER], "not found")    
  
else:
    print("Running tests")