import pyscreenshot as ImageGrab
import Image
import pytesseract

def captureScreenArea(pos_x, pos_y, length_x, length_y):
	im=ImageGrab.grab(bbox=(pos_x, pos_y, pos_x+length_x, pos_y+length_y)) # X1,Y1,X2,Y2
	return im

if __name__ == "__main__":
	capturedIm = captureScreenArea(580,150,200,50)
	extractedText = pytesseract.image_to_string(capturedIm)
	print extractedText
	if "anllne" in extractedText:
		print "Is online"
	capturedIm.show()


# print pytesseract.image_to_string(capturedIm)
# capturedIm.show()
