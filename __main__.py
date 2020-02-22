# WhatsApp Web Online Tracker
# Author: Deekshith Allamaneni / ChuckNorrison
# Email: dkhhy.d@gmail.com
# Website: https://github.com/adeekshith/whatsapp-tracker

# Preconditions Windows:
# - Install Tesseract for Windows and add to PATH env (https://github.com/UB-Mannheim/tesseract/wiki)
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
import pyscreenshot as ImageGrab
from PIL import Image
import pytesseract
import time
from datetime import datetime

dbFile = "online.csv"

def captureScreenArea(pos_x, pos_y, length_x, height_y):
    img=ImageGrab.grab(bbox=(pos_x, pos_y, pos_x + length_x, pos_y + height_y)) # X1,Y1,X2,Y2
    return img

def writeToDatabase(localtime, targetName, targetOnlineCount, targetCheckedCount):
    # Open file handle with mode append
    fo = open(dbFile, "a")
    
    #concatenate timestamp, target infos and append to file
    res = localtime + ";" + str(targetName) + ";" + targetOnlineCount + ";" + targetCheckedCount + "\n" #csv format
    fo.write(res);
    
    # Close file handle
    fo.close()
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
    if len(extractedText.split('\n'))>1:
        score += thisScoreWeight

    isOnlineAccuracy = score/maxScore
    if isOnlineAccuracy >= accuracyThreshold:
        return True
    else:
        return False
        
if __name__ == "__main__":
    # Script start
    
    # CONFIG: Screen dimensions to be captured (modify here)
    pos_x = 1355        #edit only this if you like top right alignment of WhatsApp Web Application
    pos_y = 35          #aligned top at 1920x1080
    length_x = 400      #length should be big enough for some tolerance in alignment
    height_y = 50       #height of captured screen    
    
    # Debug CONFIG: show screenshot of capture area once script gets started
    capturedImg = captureScreenArea(pos_x,pos_y,length_x,height_y)
    currentTarget = pytesseract.image_to_string(capturedImg)
    capturedImg.show() 
    print("Start online tracking of target " + currentTarget + " ...")

    timeInterval = 600 # seconds to save data to db (csv file atm)
    
    targetOnlineCount = 0 # Initializing
    targetCheckedCount = 0
    timeTargetSeenOn = datetime.now()
    targetIsOn = False
    startTime = datetime.now()

    # Looping continuously to monitor
    while True: 
        capturedImg = captureScreenArea(pos_x,pos_y,length_x,height_y)
        extractedText = pytesseract.image_to_string(capturedImg)
                
        # Online-check from capture and increase counter
        targetIsOn = checkIfOnlineFromExtractedtext(extractedText, accuracyThreshold = 0.3)
        targetCheckedCount +=1
        if targetIsOn == True:
            targetOnlineCount +=1            
        
        runTime = datetime.now()
        
        timeDif = (runTime - startTime).total_seconds()
        if timeDif > timeInterval:            
            #Log Name and Counter in a single line
            extractedText = extractedText.replace('online','')
            extractedText = extractedText.replace('online','')
            extractedText = extractedText.replace('\n','')            
            
            if targetOnlineCount != 0:
                print(timeTargetSeenOn.strftime("%d-%m-%Y %H:%M:%S: ") + extractedText + " " + str(targetOnlineCount))
            
            writeToDatabase(timeTargetSeenOn.strftime("%d-%m-%Y %H:%M:%S"), extractedText, str(targetOnlineCount), str(targetCheckedCount))
            targetOnlineCount = 0   
            targetCheckedCount = 0            
            startTime = runTime
            # remember current time to restart loop till data gets saved again (timeInterval)
            timeTargetSeenOn = datetime.now()             
        
        if currentTarget != extractedText:
            currentTarget = extractedText
            print("Start online tracking of target " + currentTarget + " ...")
        
        # sleep between each check
        time.sleep(1) #seconds
