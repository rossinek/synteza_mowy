import wave
import struct
import subprocess
import sys
import copy

from sortedcontainers import SortedList
from ..p2 import Progressbar

class WaveEditor(object):

	def __init__(self, path):
		wav = wave.open(path, "r")
		self.params = wav.getparams()
		self.bytes = wav.readframes(wav.getnframes())
		wav.close()

	def getframerate(self):
		(nchannels, sampwidth, framerate, nframes, comptype, compname) = self.params
		return framerate

	def getnvalues(self):
		return len(self.bytes)/2

	def getbytes(self):
		return self.bytes

	def append(self, bytes):
		self.bytes += bytes

	def gen_silence(self, duration):
		return "".join([struct.pack("h",0)]*int(duration*self.getframerate()))

	def duplicate(self, begin, end, n):
		new_bytes = []
		new_bytes += self.bytes[:2*begin]
		new_bytes += "".join([self.bytes[2*begin:2*end]]*n)
		new_bytes += self.bytes[2*end:]
		self.bytes = "".join(new_bytes)

	def fade_out(self, duration):
		begin = int(self.getnvalues() - duration*self.getframerate())
		if begin < 0:
			begin = 0
		new_bytes = self.bytes[:2*begin]
		fade_range = self.getnvalues()-begin
		for i in range(begin, self.getnvalues()):
			(v,) = struct.unpack("h", self.bytes[2*i:2*i+2])
			new_bytes += (struct.pack("h", int(v*(1-float(i-begin)/fade_range))))
		self.bytes = "".join(new_bytes)

	def crop(self, begin, end):
		b = int(begin*self.getframerate())
		e = int(end*self.getframerate())
		self.bytes = self.bytes[b:e]

	def save(self, path):
		wave_output = wave.open(path, "w")
		wave_output.setparams(self.params)
		wave_output.writeframes("".join(self.bytes))
		wave_output.close()

	def max_amps(self):
		max30 = SortedList()
		max30.update([(0,0)]*30)

		for i in range(0, len(self.bytes)/2):
			(v,) = struct.unpack("h", self.bytes[2*i:2*i+2])
			if (v,i) > max30[0]:
				max30.add((v,i))
				del max30[0]
		
		max_a = sorted(map(lambda (x,y): (y,x), max30[0:10]))

		last = 0
		i = 0
		while i < len(max_a):
			(index, _)=max_a[i]
			if last >= index-5:
				del max_a[i]
			else:
				i+=1
			last = index

		return max_a

	@classmethod
	def add_waves(cls, waves, display_progressbar=False):
		(sample, _) = waves[0]
		we = copy.deepcopy(sample)
		we.crop(0, 0)
		new_bytes = ''

		total_vol = 0
		max_nvalues = 0
		for (w,vol) in waves:
			total_vol+=vol
			max_nvalues = max([max_nvalues, w.getnvalues()])

		progressbar = Progressbar(50, max_nvalues)

		for i in range(0, max_nvalues):
			progressbar.update(i)
			s = 0.0
			for (w,vol) in waves:
				if len(w.bytes[2*i:2*i+2]) == 2:
					(v,) = struct.unpack("h", w.bytes[2*i:2*i+2])
					s += float(v)*vol
			s = s/total_vol
			new_bytes += struct.pack("h", int(s))
		we.bytes = new_bytes

		progressbar.finish()
		return we

	@classmethod
	def play(cls, output_path):
		if sys.platform == "darwin":
			subprocess.call(["afplay", output_path])
		elif sys.platform == "linux2":
			subprocess.call(["aplay", output_path, "-q"])
