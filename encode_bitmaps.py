#encode_bitmaps.py

#This file is derived from the wx demo version of the same thing... I just copied it !::)

import sys
from wx.tools import img2py

command_lines = [
	"-a -u -n NotebookBKGD bmp_source/BG_image.png images.py",
	"-a -u -n Splash bmp_source/splash.png images.py",
	"-a -u -n WDC bmp_source/wdc.png images.py"
	]

if __name__ == "__main__":
	for line in command_lines:
		args = line.split()
		img2py.main(args)
