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
import pyscreenshot as ImageGrab
import pytesseract as Tesseract
import time
from datetime import datetime

dbFile = "online.csv"

def captureScreenArea(pos_x, pos_y, length_x, height_y):
    img=ImageGrab.grab(bbox=(pos_x, pos_y, pos_x + length_x, pos_y + height_y)) # X1,Y1,X2,Y2
    return img

def writeCSV(targetName, onlineState, timeDif):
    targetName = targetName.replace("\n","") #pretty print tesseracted text as targetName
    # Open file handle with mode append
    fo = open(dbFile, "a")
    
    #concatenate timestamp, target infos and append to file
    printConsole("Write data: " + targetName + ";" + onlineState + ";" + timeDif)
    now = datetime.now()
    res = now.strftime("%d-%m-%Y") + ";" + now.strftime("%H:%M:%S") + ";" + targetName + ";" + onlineState + ";" + timeDif +"\n" #csv format
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
    arrText = extractedText.split('\n')
    if len(extractedText.split('\n'))>1: #this should be the second line
        if len(arrText[1]) <= 8 and len(arrText[1]) >= 4: #this should be "online" (todo: impl other lang)
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
        
if __name__ == "__main__":   
    # CONFIG: Screen dimensions to be captured (modify here)
    pos_x = 1355        #edit only this if you like top right alignment of WhatsApp Web Application
    pos_y = 35          #aligned top at 1920x1080
    length_x = 400      #length should be big enough for some tolerance in alignment
    height_y = 50       #height of captured screen    
    
    # Initializing target
    targetOnlineCount = 0
    timeTargetSeenOn = datetime.now()

    # Debug CONFIG:
    printConsole("Tesseract " + str(Tesseract.get_tesseract_version()) + " found")
    printConsole("Test capture screen area... ")
    capturedImg = captureScreenArea(pos_x,pos_y,length_x,height_y)
    printConsole("Capture screen area done! Show image...")
    capturedImg.show() 
    printConsole("Throw Tesseract on capture image")
    currentTarget = Tesseract.image_to_string(capturedImg)
    printConsole("Start online tracking of target " + currentTarget + " ...")
    
    # Looping continuously to monitor
    while True: 
        capturedImg = captureScreenArea(pos_x,pos_y,length_x,height_y)
        extractedText = Tesseract.image_to_string(capturedImg)
                        
        targetIsOn = checkIfOnlineFromExtractedtext(extractedText, accuracyThreshold = 0.3)
        now = datetime.now()
        
        #Sanitize target name
        extractedText = extractedText.replace('online','')
        extractedText = extractedText.replace('online','')
        extractedText = extractedText.replace('\n','')   
        
        if len(extractedText) == 0: #add some error handling
            printConsole("DEBUG: Cant find text in captured image")
            targetOnlineCount = 0
            timeTargetSeenOn = now
            time.sleep(0.5)            
            continue
            
        # Switch target
        if currentTarget != extractedText:
            timeDif = (now - timeTargetSeenOn).total_seconds()
            if round(timeDif) > 4: #waiting for contact infos...
                printConsole("Switch from "+currentTarget+" to new target "+extractedText)
                # write current data
                writeCSV(currentTarget, str(targetIsOn), str(round(timeDif)))
                currentTarget = extractedText
                # reset counters and timer after target was switched
                targetOnlineCount = 0
                timeTargetSeenOn = now
                continue
        
        # Online-check from capture and increase counter
        if targetIsOn == True:            
            #track online time
            targetOnlineCount +=1            
            if targetOnlineCount == 1:
                # target seen online, write to file
                timeTargetSeenOn = now  
                printConsole(extractedText + " online at " + timeTargetSeenOn.strftime("%H:%M:%S"))                  
                writeCSV(extractedText, str(targetIsOn), str(targetOnlineCount))                     
        else:
            if targetOnlineCount > 1:
                # target was online and seems offline now, write to file and reset
                timeDif = (now - timeTargetSeenOn).total_seconds()
                printConsole(extractedText + " now offline ("+str(round(timeDif))+"s online seen)") 
                writeCSV(extractedText, str(targetIsOn), str(round(timeDif)))
                targetOnlineCount = 0                
        
        # sleep between each check
        time.sleep(1) #seconds
