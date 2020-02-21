# WhatsApp tracker
# Author: Deekshith Allamaneni
# Email: dkhhy.d@gmail.com
# Website: https://github.com/adeekshith/whatsapp-tracker

# Preconditions Windows:
# - Install Tesseract for Windows and add to PATH env (https://github.com/UB-Mannheim/tesseract/wiki)
# - Install Python environment and pip install missing modules (image, pyscreenshot, pytesseract)

# Version: 2 (ChuckNorrison)
# - modifi libs to support windows python environment
# - timestamp formatted logs with Name and interval count
# - file open not as binary
# - Setup your screenposition X and Y at profile pic (pos_x=+50px) of selected chat (use capturedIm.show() to watch screenshots)

# WhatsApp tracker monitors WhatsApp users online timings and stores them to database.
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

import pyscreenshot as ImageGrab #pip install pyscreenshot
from PIL import Image #pip install image
import pytesseract
import time
from datetime import datetime

databaseFileName = "online.csv"

def captureScreenArea(pos_x, pos_y, length_x, height_y):
    im=ImageGrab.grab(bbox=(pos_x, pos_y, pos_x + length_x, pos_y + height_y)) # X1,Y1,X2,Y2
    return im

def writeToDatabase(localtime, value):
    # Open file handle with mode append
    fo = open(databaseFileName, "a")
    
    #concatenate timestamp, target infos and append to file
    res = localtime + ": " + str(value) +"\n"
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

def quantizedTime(intervalMinutes):
    localtime = time.localtime(time.time())
    return int(localtime.tm_min/intervalMinutes)

if __name__ == "__main__":
    # Initializing
    
    # Screen dimentions to be captured
    pos_x = 1350 #edit only this if you like top right alignment of WhatsApp Web Application
    pos_y = 35 #aligned top at 1920x1080
    length_x = 400 #length should be big enough for some tolerance in alignment
    height_y = 50 #height of captured screen

    # Declaring flags, variables and initializing to default values
    sleepDelay = 1 # Constant
    timeInterval = 10 # Constant: Time Interval in minutes
    
    numberOfTimesOnline = 0 # Initializing
    startTimeForThisInterval = datetime.now() # current date and time
    previousStateIsOnline = False
    presentStateIsOnline = False
    previousTimeInterval = quantizedTime(timeInterval)

    # Looping continuously to monitor
    while True:
        presentTimeInterval = quantizedTime(timeInterval)
        
        if previousTimeInterval != presentTimeInterval:
            print("Interval Changed") # Debug
            
            #Log Name and Counter in a single line
            extractedText = extractedText.replace('online','')
            extractedText = extractedText.replace('online','')
            extractedText = extractedText.replace('\n','')            
            
            writeToDatabase(startTimeForThisInterval.strftime("%d-%m-%Y %H:%M:%S"), extractedText + " " + str(numberOfTimesOnline))
            numberOfTimesOnline = 0 # Reinitializing
            previousTimeInterval = presentTimeInterval
            startTimeForThisInterval = datetime.now() # current date and time
            
        capturedIm = captureScreenArea(pos_x,pos_y,length_x,height_y)
        extractedText = pytesseract.image_to_string(capturedIm)
        
        # Debug
        print(extractedText + " " + str(numberOfTimesOnline))
        
        presentStateIsOnline = checkIfOnlineFromExtractedtext(extractedText, accuracyThreshold = 0.3)
        if presentStateIsOnline == True:
            numberOfTimesOnline +=1
        
        # Debug
        #capturedIm.show() 
        
        # Induce delay between each check
        time.sleep(sleepDelay)
