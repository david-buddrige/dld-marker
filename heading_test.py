import heading_finder


heading = "foo"
found_heading = heading_finder.find_heading(heading,"<h1>" + heading + "</h1>")
try:
    assert found_heading == True
    print("<h1> passed")  
except:
    print("<h1> did not pass")
    
    
found_heading = heading_finder.find_heading(heading,"<h2>" + heading + "</h2>")
try:
    assert found_heading == True
    print("<h2> passed")
except:
    print("<h2> did not pass")



found_heading = heading_finder.find_heading(heading,"<h3>" + heading + "</h3>")
try:
    assert found_heading == True
    print("<h3> passed")
except:
    print("<h3> did not pass")



found_heading = heading_finder.find_heading(heading,"<h3 id=\"hello\">" + heading + "</h3>")
try:
    assert found_heading == True
    print("<h3> passed")
except:
    print("<h3> did not pass")


found_heading = heading_finder.find_heading(heading," id=\"hello\">" + heading + "")
try:
    assert found_heading == False
    print("<h3> passed")
except:
    print("<h3> did not pass")
    
    
    
found_heading = heading_finder.find_heading(heading, heading)
try:
    assert found_heading == False
    print("<h3> passed")
except:
    print("<h3> did not pass")
    
html = "<p>" + heading + "</p>"
found_heading = heading_finder.find_heading(heading, html)
try:
    assert found_heading == False
    print("<p> passed")
except:
    print("<p> did not pass")

html = "<h4>" + heading + "</h4>"
found_heading = heading_finder.find_heading(heading, html)
try:
    assert found_heading == True
    print("<h4> passed")
except:
    print("<h4> did not pass")

