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
