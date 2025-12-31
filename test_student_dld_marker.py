import student_dld_marker

# THe purpose of this program is to perform a series of tests on the methods in the 
# student_dld_marker.py to confirm that each is functioning as expected.


def perform_test_get_files_in_a_directory(directory_to_check, expected_result):
    pass


directory_to_check = ".\\test_data_minimal_site_with_htm"
expected_result = ['index.htm']
files_in_directory = student_dld_marker.get_files_in_a_directory(directory_to_check)
if expected_result == files_in_directory:
    print("TEST PASSED")
else:
    print("TEST DID NOT PASS")
    
