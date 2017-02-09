"""
This is code to update the papers.rdf file that contains information
about the working paper series at Williams College.

Author: Colin Williams
Last updated: Feb 2017
"""


import os
import pickle

# TODO: Download .rdf file from server instead of storing on local machine
# TODO: Upload .rdf file automatically (and safely!)
# TODO: Generate html

# Make compatible with python2
try:
    input = raw_input
except NameError:
    pass

curYear = '2017' # Update to keep header correct
cwd = os.getcwd() + os.sep

RePEc_codes = pickle.load( open(cwd + "Faculty_Data" + os.sep + "RePEc_codes.p", "rb") )
Author_Homepage = pickle.load( open(cwd + "Faculty_Data" + os.sep + "Author_Homepage.p", "rb") )

# Read in existing papers.pdf
data = ''
with open(cwd + 'RePEc' + os.sep + 'papers.rdf', 'r') as original:
    line = original.readline() # Ignore the first line
    if curYear in original.readline(): # Check whether to update the year header
        line = original.readline() # Skip the last row of #s
        data = original.read()
        print("Year unchanged.")
    else:
        data = original.read()
        print('It\'s a new year.')
original.close()

#Rename the old file as a backup
#os.remove(cwd + "RePEc" + os.sep + "papers-old.rdf")
#os.rename(cwd + 'RePEc' + os.sep + 'papers.rdf', cwd + 'RePEc' + os.sep + 'papers-old.rdf')

###### INPUTS FOR NEW ENTRY ######
lastNames = ''
authors = int(input("How many authors?"))
for i in range (0, authors):
    firstName = input("Author first name: ")
    middleI = input("Author middle initial (no period, enter if none): ")
    lastName = input("Author last name: ")

    # Add together author last names in anticipation of the file url
    lastNames += lastName

    # Build up the full name
    fullName = firstName + " "
    if middleI:
        fullName += (middleI + ". " + lastName)
    else:
        fullName += lastName

title = input("Title: ")
# TODO: fix
#abstract = input("Abstract: ")
clasJEL = input("JEL-classification (separated by commas and spaces): ")
keywords = input("Keywords (same format): ")
length = input("Integer length: ")
# TODO: make automatic
number = input("Number (no year): ")
created = input("Creation date (yyyy-mm): ")
urlTitle = input("URL title: ")

# TODO: make into function
# Construct the new entry
with open(cwd + 'RePEc' + os.sep + 'papers-test.rdf', 'w') as modified:

    ###### OUTPUTS FOR NEW ENTRY #####
    modified.write('##################################################\n')
    modified.write("#                     "+curYear+"                       #\n")
    modified.write('##################################################\n')
    modified.write('Template-Type: ReDIF-Paper 1.0\n')

    modified.write('Author-Name: ' + fullName + '\n')
    modified.write('Author-X-Name-First: ' + firstName + '\n')
    modified.write('Author-X-Name-Last: ' + lastName + '\n')

    modified.write('Author-Person: ')
    if lastName in RePEc_codes:
        modified.write(RePEc_codes[lastName])
    modified.write('\n')

    # Williams Faculty
    if lastName in Author_Homepage: # Problems when outside authors have the same name as Williams faculty
        modified.write('Author-Workplace-Name: Williams College' + '\n')
        modified.write('Author-Workplace-Homepage: https://econ.williams.edu/profile/' + Author_Homepage[lastName] + '\n')

    # Non-Williams Faculty
    else:
        modified.write('Author-Workplace-Name: ' + '\n')
        modified.write('Author-Workplace-Homepage: ' + '\n')

    modified.write("Title: " + title + '\n')
    modified.write("Abstract: " + '\n')
    modified.write("Classification-JEL: " + clasJEL + '\n')
    modified.write("Keywords: " + keywords + '\n')
    modified.write('Length: ' + length + ' pages' + '\n')
    modified.write("Number: " + curYear + "-" + number + '\n')
    modified.write("Note: " + '\n')
    modified.write('Creation-date: ' + created + '\n')
    modified.write('Revision-date:' + '\n' + 'Price: Free' + '\n' + 'Publication-Status:' + '\n')
    modified.write('File-URL: http://web.williams.edu/Economics/wp/'+ lastNames + urlTitle + '.pdf\n')

    modified.write('File-Format: Application/PDF' + '\n')
    modified.write('File-Function: Full text' + '\n')
    modified.write('Handle: RePEc:wil:wileco:' + curYear + '-' + number + '\n\n')

    modified.write(data)

modified.close()
