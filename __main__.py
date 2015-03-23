# WhatsApp tracker
# Author: Deekshith Allamaneni
# Email: dkhhy.d@gmail.com
# Website: www.deekshith.in

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

import pyscreenshot as ImageGrab
import Image
import pytesseract
import time
import datetime

databaseFileName = "online.csv"

def captureScreenArea(pos_x, pos_y, length_x, length_y):
	im=ImageGrab.grab(bbox=(pos_x, pos_y, pos_x+length_x, pos_y+length_y)) # X1,Y1,X2,Y2
	return im

def writeToDatabase(localtime, value):
	# Open a file
	fo = open(databaseFileName, "ab")
	#localtime = time.localtime(time.time())
	timeFormatted = str(localtime.tm_year)+","+str(localtime.tm_mon)+","+str(localtime.tm_mday)+","+str(localtime.tm_hour)+","+str(localtime.tm_min)+","+str(localtime.tm_sec);
	fo.write( timeFormatted+","+str(value)+"\n");
	# Close opend file
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
	pos_x = 580
	pos_y = 150
	length_x = 200
	length_y = 50

	# Declaring flags, variables and initializing to default values
	sleepDelay = 1 # Constant
	timeInterval = 10 # Constant: Time Interval in minutes
	numberOfTimesOnline = 0 # Initializing
	startTimeForThisInterval = time.localtime(time.time())
	previousStateIsOnline = False
	presentStateIsOnline = False
	previousTimeInterval = quantizedTime(timeInterval)

	# Looping continuously to monitor
	while True:
		presentTimeInterval = quantizedTime(timeInterval)
		if previousTimeInterval != presentTimeInterval:
			writeToDatabase(startTimeForThisInterval, numberOfTimesOnline)
			numberOfTimesOnline = 0 # Reinitializing
			previousTimeInterval = presentTimeInterval
			startTimeForThisInterval = time.localtime(time.time())
		capturedIm = captureScreenArea(pos_x,pos_y,length_x,length_y)
		extractedText = pytesseract.image_to_string(capturedIm)
		print extractedText # Debug
		presentStateIsOnline = checkIfOnlineFromExtractedtext(extractedText, accuracyThreshold = 0.3)
		if presentStateIsOnline == True:
			numberOfTimesOnline +=1

		#capturedIm.show() # Debug
		# Induce delay between each check
		time.sleep(sleepDelay)
