import re              # Import the regular expression library
import os              # Import operating system library
import sys             # Import system library
from enum import Enum  # Import Enumeration library

IGNORE_FILE_OR_DIRECTORY = ['__MACOSX$','.git$','.idea$','.gitignore$','.vscode$']
DIRECTORY_ARGUMENT = '-dir'
OUTPUT_ARGUMENT = '-output'
PING_DOCS_ARGUMENT = '-pingDocs'
WEB_DEVELOPMENT_ARGUMENT = '-webdev'
REQUIRED_PARAMETER_LIST = [DIRECTORY_ARGUMENT,OUTPUT_ARGUMENT]
BOOLEAN_PARAMETER_LIST = [PING_DOCS_ARGUMENT,WEB_DEVELOPMENT_ARGUMENT]
IMAGE_TOO_BIG = 307200
IMAGE_SIZE_WARNING = 60000

# REQUIRED_DIRECTORIES = [('css'),('images','img'), ('js','javascript')]
# REQUIRED_FILES = ['index.html']

class MessageType(Enum):
    LABEL = "LABEL"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

class Message:
    
    def __init__(self, message_type, message):
        self.message_type = message_type
        self.message = message        
        
    def print(self):
        print(self.get_output_message())
  
    def get_output_message(self):
        return self.message_type.value + ",\"" + self.message.strip() + "\""

def get_name_of_current_program():
    """
    Get the name of the current program as a string

    Returns:
        string: The name of the current program.
    """
    return os.path.basename(__file__).strip()


def is_name_of_current_program(name_to_check):
    """
    
    compares the name_to_check field with the name of the current program and returns
    True if they are the same.

    Args:
        name_to_check (string): The name 

    Returns:
        _type_: _description_
    """
    return name_to_check.strip() == get_name_of_current_program()


def is_a_parameter(the_parameter, 
                   required_parameter_list = REQUIRED_PARAMETER_LIST, 
                   optional_parameter_list = BOOLEAN_PARAMETER_LIST):
    """
    Returns true if the string in "the_parameter" is one of the parameter identifiers.

    Args:
        the_parameter (string): _description_
        required_parameter_list (_type_, optional): _description_. Defaults to REQUIRED_PARAMETER_LIST.
        optional_parameter_list (_type_, optional): _description_. Defaults to BOOLEAN_PARAMETER_LIST.

    Returns:
        _type_: _description_
    """
    paramsToCheck = required_parameter_list + optional_parameter_list
    return the_parameter in paramsToCheck


def parse_arguments(required_parameter_list = REQUIRED_PARAMETER_LIST, 
                    boolean_parameter_list = BOOLEAN_PARAMETER_LIST):
    parameter_dictionary = { 
        PING_DOCS_ARGUMENT: False,
        WEB_DEVELOPMENT_ARGUMENT: False
    }
    
    next_parameter = None
    for parameter in sys.argv:
        if not is_name_of_current_program(parameter):            
            if is_a_parameter(parameter):
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


def is_valid_directory_or_file(file_or_directory_to_check, 
                               ignore_file_or_directory_list = IGNORE_FILE_OR_DIRECTORY):
    is_valid = True
    for invalid_directory in ignore_file_or_directory_list:
        is_a_match = re.search(invalid_directory, file_or_directory_to_check)
        if(is_a_match):
            is_valid = False
    return is_valid


def find_all_directories(directory_path_to_find):    
    list_of_directories = []
    if is_valid_directory_or_file(directory_path_to_find):
        list_of_directories = [directory_path_to_find]    
        all_directories = os.listdir(directory_path_to_find)
        for file_or_directory in all_directories:
            sub_path = directory_path_to_find + os.path.sep + file_or_directory
            if os.path.isdir(sub_path):            
                subList = find_all_directories(sub_path)
                list_of_directories = list_of_directories + subList
    return list_of_directories


def get_files_in_a_directory(directory_to_check):
    file_list = []
    all_files_and_directories = os.listdir(directory_to_check)
    for file_or_directory in all_files_and_directories:
        if os.path.isfile(directory_to_check + os.path.sep + file_or_directory):
            file_list.append(file_or_directory)
    return file_list


def get_directories_in_a_directory(directory_to_check):
    directory_list = []
    all_files_and_directories = os.listdir(directory_to_check)
    for file_or_directory in all_files_and_directories:
        if os.path.isdir(directory_to_check + os.path.sep + file_or_directory):
            directory_list.append(file_or_directory)
    return directory_list


def filename_is_a_webpage(filename):
    """
    Returns True if the filename ends in a .htm or .html extension and returns
    False otherwise.

    Args:
        filename (String): A string representing a filename.

    Returns:
        Boolean: True if the filename ends in .html or .htm otherwise returns False.
    """
    
    is_webpage = False
    is_website_file = re.search("html$|htm$",filename.strip(),re.RegexFlag.IGNORECASE)
    
    if is_website_file != None:            
        is_webpage = True
    return is_webpage


def files_contain_webpages(list_of_files):
    """
    This function will return True if any of the filenames in the 
    provided list_of_files is a html file.

    Args:
        list_of_files (List of String): A List of Strings. Each string represents a filename.

    Returns:
        boolean: True if any of the files are html files, or else False.
    """
    is_website_folder = False
    
    for filename in list_of_files:    
        if filename_is_a_webpage(filename):
            is_website_folder = True
            break
    return is_website_folder
    

def is_a_website_folder(directory_to_check):
    """
    This function will return True if the directory provided contains at least one html file.
    
    Args:
        directory_to_check (String): A String representing a directory path.

    Returns:
        _type_: _description_
    """
    is_website_folder = False
    file_list = get_files_in_a_directory(directory_to_check)
    is_website_folder =  files_contain_webpages(file_list)
    return is_website_folder


def check_for_file_or_directory(name_to_find, directory_location, list_of_files_or_directories):
    message_to_return = None
    if name_to_find in list_of_files_or_directories:
        message_to_return = Message(MessageType.INFO, name_to_find + " found in " + directory_location)
    else:
        message_to_return = Message(MessageType.ERROR, name_to_find + " not found in " + directory_location)
    return message_to_return


def check_for_valid_file_or_directory_from_list(list_of_valid_names, directory_location, list_of_files_or_directories):
    message_to_return = check_for_file_or_directory(list_of_valid_names[0], directory_location, list_of_files_or_directories)
    if message_to_return.message_type == MessageType.ERROR:
        # Then check the other options
        for name_option_index in range(1,len(list_of_valid_names)):
            message_option_2 = check_for_file_or_directory(list_of_valid_names[name_option_index], directory_location,list_of_files_or_directories)
            if message_option_2.message_type != MessageType.ERROR:
                # Then we have found one of the acceptable options
                message_to_return = message_option_2
                break
    return message_to_return


def check_for_div(html_file_line):   
    div_found = False
    has_div = re.search("<div", html_file_line, re.RegexFlag.IGNORECASE)
    if has_div != None:
        div_found = True
    return div_found


def check_for_span(html_file_line):
    # Check for <span>
    has_span = False
    hasSpan = re.search("<span", html_file_line, re.RegexFlag.IGNORECASE)
    if(hasSpan != None):
        has_span = True
    return has_span


def check_for_img(html_file_line):
    img_found = False
    has_img = re.search("<img\\s.+>|<img\\s", html_file_line, re.RegexFlag.IGNORECASE)
    if has_img != None:
        # Then we have an <img> tag.
        img_found = True
    return img_found


def has_alt_property(line):
    alt_found = False
    has_alt = re.search("\\salt[\\s]*=",line, re.RegexFlag.IGNORECASE)
    if has_alt != None:
        alt_found = True
    return alt_found


def has_style_property(line):
    has_style = re.search("\\sstyle=[\"\'].*[\"\']",line)
    if (has_style):
        return True
    else:
        return False
            
            
def has_width_property(line):
    has_width = re.search("\\swidth=[\"\'].*[\"\']",line)
    if (has_width):
        return True
    else:
        return False

def has_height_property(line):
    has_height = re.search("\\sheight=[\"\'].*[\"\']",line)
    if (has_height):
        return True
    else:
        return False

            
def has_upper_case_tag(line):
    has_upper_case_tag = False
    upper_case_tag = re.search("<[A-Z]+",line)
    if(upper_case_tag != None):
        has_upper_case_tag = True
    return has_upper_case_tag


# This function will take the path of a html file and perform checks on its contents.
# It will return a list of messages with information or errors about the html file.

def check_html_file(html_file):
    message_list = [Message(MessageType.INFO, "Process html file: " + html_file)]
    file_name_only = os.path.basename(html_file)
    div_count = 0
    line_number = 0
    with open(html_file, encoding="utf8") as the_html_file:
        for text_line in the_html_file:  
            line_number += 1
            
            if check_for_div(text_line):
                div_count += 1
                if(div_count > 1):
                    div_message = Message(MessageType.ERROR,file_name_only + "(" + str(line_number) +  "): MULTIPLE <DIV> LOCATED: More than one <div> found on line " + str(line_number) + " of file: " + html_file + "' in violation of standards.  This is <div> number " + str(div_count) )
                    message_list.append(div_message)
                    div_message = Message(MessageType.ERROR,text_line)
                    message_list.append(div_message)
            
            if check_for_span(text_line):
                file_name_only = os.path.basename(html_file)
                span_message = Message(MessageType.WARNING, file_name_only + "(" + str(line_number) +  "): <SPAN> LOCATED: <span> found on line "  + str(line_number) + " of file: '" + html_file + "' in violation of standards.")
                message_list.append(span_message)
                span_message = Message(MessageType.WARNING, text_line)
                message_list.append(span_message)
            
            if check_for_img(text_line):
                if has_alt_property(text_line) == False:
                    missing_alt_message = Message(MessageType.ERROR,file_name_only + "(" + str(line_number) +  "): POSSIBLE MISSING ALT - check next line of html: <img> missing alt on line "  + str(line_number) + " of file: " + html_file)
                    message_list.append(missing_alt_message)
                    missing_alt_message = Message(MessageType.ERROR,text_line)
                    message_list.append(missing_alt_message)
                    
                if has_height_property(text_line):
                    has_height_message = Message(MessageType.ERROR, file_name_only + "(" + str(line_number) +  "): HEIGHT PROPERTY IN HTML- The height property should be specified in your css, not in your html."  + str(line_number) + " of file: " + html_file)
                    message_list.append(has_height_message)
                    has_height_message = Message(MessageType.ERROR, text_line)
                    message_list.append(has_height_message)

                if has_width_property(text_line):
                    has_width_message = Message(MessageType.ERROR,file_name_only + "(" + str(line_number) +  "): WIDTH PROPERTY IN HTML- The width property should be specified in your css, not in your html."  + str(line_number) + " of file: " + html_file)
                    message_list.append(has_width_message)
                    has_width_message = Message(MessageType.ERROR,text_line)  
                    message_list.append(has_width_message)

            if has_upper_case_tag(text_line):
                has_upper_case_message = Message(MessageType.ERROR,file_name_only + "(" + str(line_number) +  "): UPPER CASE HTML: found on line "  + str(line_number) + " of file: " + html_file)
                message_list.append(has_upper_case_message)
                has_upper_case_message = Message(MessageType.ERROR,text_line)
                message_list.append(has_upper_case_message)
               
    return message_list

    
def check_website_for_required_directories_and_files(directory_to_check, all_website_directories, all_website_files):
    message_list = [] 
        
    # Check for index.html
    index_message = check_for_valid_file_or_directory_from_list(["index.html","index.htm"], directory_to_check, all_website_files)
    message_list.append(index_message)

    # Check for css folder
    # print("All directories:")
    # print(all_directories)
    css_message = check_for_file_or_directory("css", directory_to_check, all_website_directories)
    message_list.append(css_message)

    # Check for js folder
    js_message =  check_for_valid_file_or_directory_from_list(["js","javascript"], directory_to_check, all_website_directories)        
    message_list.append(js_message)
        
    # Check for images folder
    images_message = check_for_valid_file_or_directory_from_list(["img","images"], directory_to_check, all_website_directories)
    message_list.append(images_message)
        
    return message_list


def check_each_webpage_in_the_website(website_directory, list_of_web_files):
    messages = []
    # check each webpage in the website
    for web_file in list_of_web_files:
        if filename_is_a_webpage(web_file):
            full_path_of_web_file = website_directory + os.path.sep + web_file
            web_file_messages = check_html_file(full_path_of_web_file)
            messages.extend(web_file_messages)
    return messages


def output_messages(list_of_messages, output_filename):
    with open(output_filename, "w") as output_file:
        output_file.write('"MessageType","Message"\n')
        for message_item in list_of_messages:
            output_file.write(message_item.get_output_message() + "\n")

if __name__ == "__main__":
    message_list = []
    
    # print("starting")
    process_message = Message(MessageType.INFO, "Running " + get_name_of_current_program()) 
    message_list.append(process_message)

    # print("MessageCode, Message")
    parameter_dictionary = parse_arguments()
    
    if(os.path.exists(parameter_dictionary[DIRECTORY_ARGUMENT])):    
        # print("directory exists")

        process_message = Message(MessageType.INFO,"Processing " + parameter_dictionary[DIRECTORY_ARGUMENT])
        message_list.append(process_message)
        all_directories = find_all_directories(parameter_dictionary[DIRECTORY_ARGUMENT])
        #print(all_directories)
        for directory in all_directories:
            if is_a_website_folder(directory):
                # Apply processing website message
                website_process_message = Message(MessageType.INFO,"Processing website directory :" + directory)
                message_list.append(website_process_message)
                
                # Get the files and directories in the website folder
                all_website_directories = get_directories_in_a_directory(directory)
                all_web_files = get_files_in_a_directory(directory)
                
                # Check if the website has the necessary files and folders 
                messages = check_website_for_required_directories_and_files(directory, all_website_directories, all_web_files)
                message_list.extend(messages)
                
                web_file_messages = check_each_webpage_in_the_website(directory, all_web_files)
                # Add the messages about the web page to the list of messages
                message_list.extend(web_file_messages)
                
    output_messages(message_list, parameter_dictionary[OUTPUT_ARGUMENT])

