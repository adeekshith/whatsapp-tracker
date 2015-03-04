import pyscreenshot as ImageGrab
from StringIO import StringIO

def captureScreenArea(pos_x, pos_y, length_x, length_y):
	im=ImageGrab.grab(bbox=(pos_x, pos_y, pos_x+length_x, pos_y+length_y)) # X1,Y1,X2,Y2
	im.show()

captureScreenArea(10,10,100,100)