#!/usr/bin/env python3

#Search for text into SFOS Calendar.
 
#Script: Ric9k. Very basic. Very noob. Remarks welcome! 


import sqlite3
import sys # For variables passed to the script
from os.path import exists # To verify if the file exists
import os #Launch shell commands, to check if we are root or user, for the home path
#import subprocess #Launch shell commands, to check if we are root or user
import datetime #To convert epoch in a readable date/time format
#args = ['a', 'a']
args = sys.argv

debug = 0
firstNameString = ''
lastNameString = ''

userHome=os.environ['HOME']
#Below not working 
#calDb = userHome+'/.local/share/system/privileged/Calendar/mkcal/db' #Real
calDb = '/home/defaultuser/.local/share/system/privileged/Calendar/mkcal/db' #Real
#Check if executed as root
command = ("whoami")
whoAmI = os.popen(command).read()

print('  ')
print('Sailfish Calendar Search')
print('-----------------------------')
print('  ')
print('-t     display text found into Calendar events')
print('  ')
print('Accents sensitive search.')
print('  Wildcards:')
print('  Use "_" for single character')
print('  Use "%" for multiple characters')
print('  ')

if debug == 1:
    searchTerms = ['Hello', '', '']
    searchNames = ''
elif debug == 0:
    #Ask user to enter the terms he want to search
    searchTerms = ['']
    newTerm = 'a'
    i = 0
    while (newTerm != ""):
        i += 1
        if i == 1:
            newTerm =  input("Search for: ")
            if newTerm == '':
                print('Nothing to search, aborting.')
                exit()
        elif i > 1:
            print('Add a search term,')
            newTerm =  input("or leave empty if done: ")
        searchTerms.append(newTerm)
        #We allow a max of 3 terms
        if len(searchTerms) == 4:
            break

#Verify if needed files exist, try with nemo username (Not sure this works, actually!)
if not exists(calDb):
    print('No defaultuser db. Trying nemo')
    calDb = '/home/nemo/.local/share/system/privileged/Calendar/mkcal/db' #Real
    if not exists(calDb):
        print('Calendar database cannot be found. Aborting')

#Open databases
calConnection = sqlite3.connect(calDb)
calCursor = calConnection.cursor()

#Remove empty entries and make all lowercase
searchTermsCleaned = []
for element in searchTerms:
    if element != '':
        searchTermsCleaned.append(element)

if len(searchTermsCleaned) == 1:
    #print(1)
    calCursor.execute("""SELECT Summary, Description, DateStart, Location FROM Components WHERE (Summary LIKE '%'||?||'%' OR Description LIKE '%'||?||'%' OR Location LIKE '%'||?||'%')""", [searchTermsCleaned[0], searchTermsCleaned[0], searchTermsCleaned[0]])
    foundTextTable = calCursor.fetchall()
elif len(searchTermsCleaned) == 2:
    calCursor.execute("""SELECT Summary, Description, DateStart, Location FROM Components WHERE (Summary LIKE '%'||?||'%' OR Description LIKE '%'||?||'%' OR Location LIKE '%'||?||'%') AND (Summary LIKE '%'||?||'%' OR Description LIKE '%'||?||'%' OR Location LIKE '%'||?||'%')""", [searchTermsCleaned[0], searchTermsCleaned[0], searchTermsCleaned[0], searchTermsCleaned[1], searchTermsCleaned[1], searchTermsCleaned[1]])
    foundTextTable = calCursor.fetchall() 
elif len(searchTermsCleaned) == 3:
    calCursor.execute("""SELECT Summary, Description, DateStart, Location FROM Components WHERE (Summary LIKE '%'||?||'%' OR Description LIKE '%'||?||'%' OR Location LIKE '%'||?||'%') AND (Summary LIKE '%'||?||'%' OR Description LIKE '%'||?||'%' OR Location LIKE '%'||?||'%') AND (Summary LIKE '%'||?||'%' OR Description LIKE '%'||?||'%' OR Location LIKE '%'||?||'%')""", [searchTermsCleaned[0], searchTermsCleaned[0], searchTermsCleaned[0], searchTermsCleaned[1], searchTermsCleaned[1], searchTermsCleaned[1], searchTermsCleaned[2], searchTermsCleaned[2], searchTermsCleaned[2]])
    foundTextTable = calCursor.fetchall() 
    ##print(2)
    #calCursor.execute("""SELECT remoteUid, endTime, freeText FROM Events WHERE (freeText LIKE '%'||?||'%' AND freeText LIKE '%'||?||'%')""", [searchTermsCleaned[0], searchTermsCleaned[1]])
    #foundTextTable = calCursor.fetchall()
#elif len(searchTermsCleaned) == 3:
    ##print(3)
    #calCursor.execute("""SELECT remoteUid, endTime, freeText FROM Events WHERE (freeText LIKE '%'||?||'%' AND freeText LIKE '%'||?||'%' AND freeText LIKE '%'||?||'%')""", [searchTermsCleaned[0], searchTermsCleaned[1], searchTermsCleaned[2]])
    #foundTextTable = calCursor.fetchall()

#Search for correspondant's name, message date, text

numbersTable = []
numbersTable.append(0)
resultCount = -1
for textSearchLine in foundTextTable:

    #Convert epoch time to a more readable time format
    msgTime = datetime.datetime.fromtimestamp(textSearchLine[2])
    resultCount += 1
    print('''\n''''Result #',resultCount,'---------')
    print(msgTime)
    print(textSearchLine[0]) #Summary
    print(textSearchLine[1]) #Description
            
    #Launch jolla-messages into the chosen conversation - Not always working        
    #Temporarly store the search number aside phone number
    #numbersTable.append(textSearchLine[0])
#print('Go to conversation?')
#print('This will create a new message.')
#print('''Don't press send!''')
#wantedNumber = int(input('Enter result #:'))
#command = ('dbus-send --type=method_call --dest=org.nemomobile.qmlmessages / org.nemomobile.qmlmessages.startSMS array:string:"'+numbersTable[wantedNumber]+'" string:" "')
#os.system(command)

if calConnection:
    calConnection.close()
