# WhatsApp Web Online Tracker
# Author: Deekshith Allamaneni / ChuckNorrison
# Email: dkhhy.d@gmail.com
# Website: https://github.com/adeekshith/whatsapp-tracker

# Preconditions Windows:
# - Install Tesseract for Windows and add to PATH env (https://github.com/UB-Mannheim/tesseract/wiki)
#   If you don't have tesseract executable in your PATH, include the following:
#   pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
#   Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
# - Install Python environment and pip install missing modules (image, pyscreenshot, pytesseract)

# WhatsApp Web Online Tracker monitors WhatsApp users online timings and stores them to database.
# Copyright (C) 2015  Deekshith Allamaneni 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# use pip install for missing modules

#system imports
import re
import time
from datetime import datetime
from pathlib import Path
import os

#third party imports
import pyscreenshot as ImageGrab
import pytesseract as Tesseract

# CONFIG: Screen dimensions to be captured (modify here)
POS_X = 1355            #edit only this if you like top right alignment of WhatsApp Web Application
POS_Y = 35              #aligned top at 1920x1080
LENGTH_X = 400          #length should be big enough for some tolerance in alignment
HEIGHT_Y = 54           #height of captured screen
WRITE_INTERVAL = 600    #optional: interval in seconds to force write

#initialize global vars (does not need modification)
dbFile = "online.csv"
targetOnlineCount = 0
timeInterval = datetime.now()
targetWasOn = False
currentTarget = ""
nextTarget = ""

def captureScreenArea():
    img=ImageGrab.grab(bbox=(POS_X, POS_Y, POS_X + LENGTH_X, POS_Y + HEIGHT_Y)) # X1,Y1,X2,Y2
    return img

def setupCSV():
    try:
        size = os.path.getsize(dbFile)
        printConsole("db file with size of " + str(size) + " found")
    except (OSError, IOError) as e:
        printConsole("DEBUG: " + str(e))
        printConsole("Try to create dbFile with headline...")
        #create file with headline
        with open(dbFile, 'w') as fo:
            res = "date;time;target;online;seconds\n"
            fo.write(res)
        fo.close()      
        printConsole("dbFile created successful as " + dbFile) 
        
    return
    
def writeCSV(targetName, onlineState, timeDif):
    targetName = targetName.replace("\n","") #pretty print tesseracted text as targetName
    try:
        # Open file handle with mode append
        fo = open(dbFile, "a")
        #concatenate timestamp, target infos and append to file
        printConsole("Write data: " + targetName + ";" + onlineState + ";" + timeDif)
        now = datetime.now()
        res = now.strftime("%d-%m-%Y") + ";" + now.strftime("%H:%M:%S") + ";" + targetName + ";" + onlineState + ";" + timeDif +"\n" #csv format
        fo.write(res);
        fo.close()
    except (OSError, IOError) as e:
        printConsole("DEBUG: " + str(e))
        
    return

def checkIfOnlineFromExtractedtext(extractedText, accuracyThreshold=0.5):
    score = 0.0 # Initializing
    maxScore = 0.0 # Initializing. Not actual max score

    # Test 1 using OCR character matching
    thisScoreWeight = 1
    maxScore += thisScoreWeight
    if "anllne" in extractedText or "anlme" in extractedText or "online" in extractedText:
        score += thisScoreWeight
        
    # Test 2 which assumes that the second line 
    # in the extracted OCR text is "online"
    # This method works when the OCR algorithm 
    # does not perform well. This is usually the case.
    thisScoreWeight = 2
    maxScore += thisScoreWeight
    arrText = extractedText.split('\n')
    if len(arrText)>1: #check status line is set
        if len(arrText[1]) <= 8 and len(arrText[1]) >= 4: #this should be "online" (todo: impl other lang. a word 4-8 chars will result true is not great)
            score += thisScoreWeight    
        
    isOnlineAccuracy = score/maxScore
    if isOnlineAccuracy >= accuracyThreshold:
        return True
    else:
        return False

def printConsole(strMsg):
    now = datetime.now()
    print(now.strftime("%d-%m-%Y %H:%M:%S: ") + strMsg)
    return
    
def sanitizeTargetName(targetName):
    arrTargetText = targetName.split('\n')
    if len(arrTargetText)>1: #check if a second line was found
        targetName = arrTargetText[0] #first line is our targetName
    else:
        #in all other cases we try to simple string replace with regexp patterns
        rep_dict = {
            'klicke hier für Kontaktinfos':'',
            'Klicke hier fiir Kontaktinfo':'',
            'klicke hier fur Kontaktinfo':'',
            'online':'',
            'anllne':'',
            'anlme':'',
            '\n':''
            }
        pattern = re.compile("|".join([re.escape(k) for k in sorted(rep_dict,key=len,reverse=True)]), flags=re.DOTALL)
        targetName = pattern.sub(lambda x: rep_dict[x.group(0)], targetName)
        
    return targetName
    
def resetInterval():
    global timeInterval, targetOnlineCount, currentTarget
    if currentTarget != "":
        timeDifIt = (datetime.now() - timeInterval).total_seconds()
        writeCSV(currentTarget, str(targetWasOn), str(round(timeDifIt)))
    currentTarget = nextTarget
    # reset counters and timer after target was switched
    targetOnlineCount = 0
    timeInterval = datetime.now()
    return
    
if __name__ == "__main__":
    setupCSV()
    
    # Debug CONFIG:
    printConsole("Tesseract " + str(Tesseract.get_tesseract_version()) + " found")
    printConsole("Test capture screen area... ")
    capturedImg = captureScreenArea()
    printConsole("Capture screen area done! Show image...")
    capturedImg.show() 
    printConsole("Throw Tesseract on capture image")
    extractedText = Tesseract.image_to_string(capturedImg)
    currentTarget = sanitizeTargetName(extractedText)
    printConsole("Start online tracking of target " + currentTarget + " ...")
    targetIsOn = checkIfOnlineFromExtractedtext(extractedText, accuracyThreshold = 0.3)
    
    # Looping continuously to monitor
    while True: 
        capturedImg = captureScreenArea()
        extractedText = Tesseract.image_to_string(capturedImg)
        targetWasOn = targetIsOn                     
        now = datetime.now()        
        
        if len(extractedText) == 0: #add some error handling
            printConsole("DEBUG: Cant find text in captured image")
            currentTarget = ""
            resetInterval()
            time.sleep(0.5)            
            continue
            
        #Sanitize target name (todo: language)
        nextTarget = sanitizeTargetName(extractedText)
            
        # Switch target
        if currentTarget != nextTarget:
            printConsole("Switch from '"+currentTarget+"' to new target '"+nextTarget+"'")
            resetInterval()
            continue
            
        #Interval reset
        if WRITE_INTERVAL != 0:
            timeDifInterval = (now - timeInterval).total_seconds()
            if timeDifInterval > WRITE_INTERVAL:
                printConsole("Interval " + str(WRITE_INTERVAL) + " reached")
                resetInterval()
            continue
        
        # Online-check from capture and increase counter
        targetIsOn = checkIfOnlineFromExtractedtext(extractedText, accuracyThreshold = 0.3)
        if targetIsOn == True:            
            #track online time
            targetOnlineCount +=1            
            if targetOnlineCount == 1:
                # target is online start stopwatch as timeInterval
                timeInterval = now  
                printConsole(currentTarget + " online")
                writeCSV(currentTarget, "True", "1")
        else:
            if targetOnlineCount > 1:
                # target was online and seems offline now, write to file and reset
                timeDif = (now - timeInterval).total_seconds()
                printConsole(currentTarget + " now offline ("+str(round(timeDif))+"s online seen)") 
                writeCSV(currentTarget, str(targetWasOn), str(round(timeDif)))
                targetOnlineCount = 0 
                
        # sleep between each check (modify for your needs... check performance)
        time.sleep(0.2) #seconds
