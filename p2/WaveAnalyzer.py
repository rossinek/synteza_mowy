import struct
import math

from ..p1.WaveEditor import WaveEditor

class WaveAnalyzer(WaveEditor):
		
	def __init__(self, path):
		WaveEditor.__init__(self, path)

	def split(self, parts=2):
		pass
	
	def rms(self, begin, n=10):
		sqrt((a1^2+...+an^2)/n)
