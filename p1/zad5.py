# -*- coding: utf-8 -*-

import sys
import subprocess
import re

from WaveEditor import WaveEditor

print "ZAD5: Przedłużanie samogłoski"

try:
	duration = float(input("Czas przedłużenia (-1): "))
except:
	duration = -1
while duration >= 0:
	we = WaveEditor("fonemy2016/e.wav")
	duration_difference = duration*we.getframerate() - we.getnvalues()
	if duration_difference < 0:
		we.crop(0, duration)
		we.fade_out(0.1)
	else:
		max_amps = we.max_amps()
		(begin,_) = max_amps[0]
		(end,_) = max_amps[3]
		n = int(duration_difference/(end-begin))
		we.duplicate(begin, end, n)
	
	we.save("output.wav")
	WaveEditor.play("output.wav")
		
	try:
		duration = float(input("Czas przedłużenia (-1): "))
	except:
		duration = -1