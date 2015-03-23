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

def captureScreenArea(pos_x, pos_y, length_x, length_y):
	im=ImageGrab.grab(bbox=(pos_x, pos_y, pos_x+length_x, pos_y+length_y)) # X1,Y1,X2,Y2
	return im

if __name__ == "__main__":
	# Initializing
	
	# Screen dimentions to be captured
	pos_x = 580
	pos_y = 150
	length_x = 200
	length_y = 50

	# Declaring flags and variables and initialize to default values
	foundOnline = False
	defaultSleepDelay = 1
	sleepDelayWhenFoundOnline = 30
	sleepDelay = defaultSleepDelay

	# Looping continuously to monitor
	while True:
		capturedIm = captureScreenArea(pos_x,pos_y,length_x,length_y)
		extractedText = pytesseract.image_to_string(capturedIm)
		#print extractedText
		if "anllne" in extractedText or "anlme" in extractedText or "online" in extractedText:
			print extractedText
			print "Is online"
			foundOnline = True
			sleepDelay = sleepDelayWhenFoundOnline
			# Open a file
			fo = open("online.txt", "ab")
			fo.write( str(datetime.datetime.now())+","+"\n");
			# Close opend file
			fo.close()
		else:
			foundOnline = False
			sleepDelay = defaultSleepDelay
		#capturedIm.show()
		time.sleep(sleepDelay)
