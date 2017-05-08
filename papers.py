"""
This is code to update the papers.rdf file that contains information
about the working paper series at Williams College.

Author: Colin Williams
Last updated: April 2017
"""

import os
import pickle
import datetime
# import paramiko

# TODO: Download .rdf file from server instead of storing on local machine
# TODO: Upload .rdf file automatically (and safely!)
# DONE: Generate html
# TODO: get the year from sys

# Takes two arguments: a list of paper information in the order of paper number,
# paper address, and paper title, as in ['01', 'http://...', 'Title']; and a
# list of authors in alphabetical order
def genHTML(paperInfo = [], authors = []):
    authorString = authors[0]
    for i in range(1, len(authors), 1):
        if (i == len(authors) - 1): # last author
            if len(authors) == 2:
                authorString += " and " + authors[i]
            else:
                authorString += ", and " + authors[i]
        else:
            authorString += ", " + authors[i]

    html = paperInfo[0] + " -- <a href=\"" + paperInfo[1] + "\">" + paperInfo[2] + "</a>. " + authorString + "."
    return html

# The 'test' argument specifies whether the output will be written to
# the actual .rdf file or whether it will be to a test file. For now,
# the default is to a test file.
def addNewEntry(entry = "", curYear = "2017", test = "-test"):
    cwd = os.getcwd() + os.sep

    # Read in existing papers.pdf
    data = ''
    with open(cwd + 'RePEc' + os.sep + 'papers.rdf', 'r') as original:
        line1 = original.readline() # Ignore the first line of #s
        line2 = original.readline()
        if curYear in line2: # Check whether to update the year header
            line3 = original.readline() # Skip the last row of #s
            data = original.read()
            print("Year unchanged: " + curYear)
        else:
            data = line1 + line2 + original.read()
            print('It\'s a new year: ' + curYear)
    original.close()

    # Write the new entry to the file
    with open(cwd + 'RePEc' + os.sep + 'papers' + test + '.rdf', 'w') as modified:

        ###### OUTPUTS FOR NEW ENTRY #####
        modified.write('##################################################\n')
        modified.write("#                     "+curYear+"                       #\n")
        modified.write('##################################################\n')
        modified.write('Template-Type: ReDIF-Paper 1.0\n')

        modified.write(entry + '\n\n')
        modified.write(data)

    modified.close()

# A function that replaces the .rdf on the Williams server with the one found
# on the local machine.
"""
def uploadRDF():
    ssh = paramiko.SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect(server, username=username, password=password)
    sftp = ssh.open_sftp()
    sftp.put(localpath, remotepath)
    sftp.close()
    ssh.close()
"""

###############################################################################
# Simple code to add an entry through the command line. Works
# on Windows and Linux, but is unable to read in the abstract due to its length.
###############################################################################
# Make compatible with python2.
try:
    input = raw_input
except NameError:
    pass

def simpleAddEntry():
    curYear = '2017' # Update to keep header correct
    cwd = os.getcwd() + os.sep

    RePEc_codes = pickle.load( open(cwd + "Faculty_Data" + os.sep + "RePEc_codes.p", "rb") )
    Author_Homepage = pickle.load( open(cwd + "Faculty_Data" + os.sep + "Author_Homepage.p", "rb") )

    # Read in existing papers.pdf
    data = ''
    with open(cwd + 'RePEc' + os.sep + 'papers.rdf', 'r') as original:
        line1 = original.readline() # Ignore the first line
        line2 = original.readline()
        if curYear in line2: # Check whether to update the year header
            line3 = original.readline() # Skip the last row of #s
            data = original.read()
            print("Year unchanged: " + curYear)
        else:
            data = line1 + line2 + original.read()
            print('It\'s a new year: ' + curYear)
    original.close()

    #Rename the old file as a backup
    #os.remove(cwd + "RePEc" + os.sep + "papers-old.rdf")
    #os.rename(cwd + 'RePEc' + os.sep + 'papers.rdf', cwd + 'RePEc' + os.sep + 'papers-old.rdf')

    ###### INPUTS FOR NEW ENTRY ######
    lastNames = ''
    firstName, middleI, lastName, fullNameList = [], [], [], []
    numAuthors = int(input("How many authors?"))
    for i in range (0, numAuthors):
        firstName.append(input("Author first name: "))
        middleI.append(input("Author middle initial (no period, enter if none): "))
        lastName.append(input("Author last name: "))

        # Add together author last names in anticipation of the file url
        lastNames += lastName[i]

        # Build up the full name
        fullName = firstName[i] + " "
        if middleI[i]:
            fullName += (middleI[i] + ". " + lastName[i])
        else:
            fullName += lastName[i]
        fullNameList.append(fullName)

    title = input("Title: ")
    clasJEL = input("JEL-classification (separated by commas and spaces): ")
    keywords = input("Keywords (same format): ")
    length = input("Integer length: ")
    # TODO: make automatic
    number = input("Number (no year): ")
    created = input("Creation date (yyyy-mm): ")
    urlTitle = input("URL title: ")

    # Construct the new entry
    with open(cwd + 'RePEc' + os.sep + 'papers-test.rdf', 'w') as modified:

        ###### OUTPUTS FOR NEW ENTRY #####
        modified.write('##################################################\n')
        modified.write("#                     "+curYear+"                       #\n")
        modified.write('##################################################\n')
        modified.write('Template-Type: ReDIF-Paper 1.0\n')

        for i in range(0, numAuthors):
            modified.write('Author-Name: ' + fullNameList[i] + '\n')
            modified.write('Author-X-Name-First: ' + firstName[i] + '\n')
            modified.write('Author-X-Name-Last: ' + lastName[i] + '\n')

            modified.write('Author-Person: ')
            if lastName[i] in RePEc_codes:
                modified.write(RePEc_codes[lastName[i]])
            modified.write('\n')

            # Williams Faculty
            if lastName[i] in Author_Homepage: # Problems when outside authors have the same name as Williams faculty
                modified.write('Author-Workplace-Name: Williams College' + '\n')
                modified.write('Author-Workplace-Homepage: https://econ.williams.edu/profile/' + Author_Homepage[lastName[i]] + '\n')
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

###############################################################
def main():
    simpleAddEntry()
if __name__ == '__main__':
    main()
