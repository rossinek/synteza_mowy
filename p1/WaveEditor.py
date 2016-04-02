import wave
import struct
import subprocess
import sys
import copy
import types

from sortedcontainers import SortedList
from ..p2.Progressbar import Progressbar

class WaveEditor(object):

	def __init__(self, arg):
		if isinstance(arg, types.StringType):
			path = arg
			wav = wave.open(path, "r")
			self.params = wav.getparams()
			bytes = wav.readframes(wav.getnframes())
			self.init_values(bytes)
			wav.close()
		elif isinstance(arg, types.TupleType):
			self.params = arg
			self.values = []
		else:
				raise ValueError('Wrong argument for constructor (WaveEditor)')
	def __getitem__(self, index):
		return self.values[index[0]*self.getnchannels()+index[1]]

	def getparams(self):
		return self.params

	def getframerate(self):
		(nchannels, sampwidth, framerate, nframes, comptype, compname) = self.params
		return framerate
	
	def getnchannels(self):
		(nchannels, sampwidth, framerate, nframes, comptype, compname) = self.params
		return nchannels
	
	def getnvalues(self):
		return len(self.values)/self.getnchannels()

	def init_values(self, bytes):
		nchannels = self.getnchannels()
		self.values = list(struct.unpack(str(len(bytes)/2)+'h', bytes))

		#for i in range(0, len(bytes)/(2*nchannels)):
		#	val = list(struct.unpack(str(nchannels)+'h', bytes[i*2*nchannels:i*2*nchannels+nchannels*2]))
		#	self.values.append(val)

	def packbytes(self):
		#flat_values = WaveEditor.flatten(self.values)
		max_v = max([max(self.values), abs(min(self.values))])
		if max_v > 32767.0:
			factor = 32767.0/max_v
			map((lambda v: v*factor), self.values)
		
		return struct.pack('%sh' % len(self.values), *self.values)

	def getvalues(self):
		return self.values

	def concat(self, values):
		self.values += values

	def gen_silence(self, duration):
		return [0.0]*(self.getnchannels()*int(duration*self.getframerate()))

	def duplicate(self, begin, end, n):
		self.values = self.values[:(begin*self.getnchannels())]+self.values[(begin*self.getnchannels()):(end*self.getnchannels())]*n+self.values[(end*self.getnchannels()):]

	def fade_out(self, duration):
		begin = int(self.getnvalues() - duration*self.getframerate())
		if begin < 0:
			begin = 0
		new_values = self.values[:(begin*self.getnchannels())]
		fade_range = self.getnvalues()-begin
		for i in range(begin, self.getnvalues()):
			for c in range(0, self.getnchannels()):
				factor = (1.0-float(i-begin)/fade_range)
				new_values.append(self[i, c]*factor*factor)
		self.values = new_values

	def crop(self, begin, end):
		b = int(begin*self.getframerate())
		e = int(end*self.getframerate())
		self.values = self.values[(b*self.getnchannels()):(e*self.getnchannels())]

	def mult(self, factor):
		self.values = map(lambda x: x*factor, self.values)
	
	def save(self, path):
		wave_output = wave.open(path, "w")
		wave_output.setparams(self.params)
		wave_output.writeframes(self.packbytes())
		wave_output.close()

	@classmethod
	def add_waves(cls, waves, verbose=False):
		(sample, _) = waves[0]
		we = WaveEditor(sample.getparams())

		total_vol = 0.0
		max_nvalues = 0.0
		for (w,vol) in waves:
			total_vol+=vol
			max_nvalues = max([max_nvalues, len(w.values)])

		if verbose:
			print "Settings volumes..."
			progressbar = Progressbar(50, len(waves))

		wvalues = []
		for (w,vol) in waves:
			w.mult(float(vol)/total_vol)
			if len(w.values)<max_nvalues:
				w.concat([0.0]*(max_nvalues-len(w.values)))
			wvalues.append(w.values)
			if verbose:
				progressbar.update_add1()

		if verbose:
			progressbar.finish()

		if verbose:
			print "Adding waves..."

		we.values = map(sum, zip(*wvalues))
		return we

	@classmethod
	def play(cls, output_path):
		if sys.platform == "darwin":
			subprocess.call(["afplay", output_path])
		elif sys.platform == "linux2":
			subprocess.call(["aplay", output_path, "-q"])
	'''
	@classmethod
	def flatten(cls, lst):
		flat = []
		for x in lst:
			if hasattr(x, '__iter__') and not isinstance(x, basestring):
				flat.extend(cls.flatten(x))
			else:
				flat.append(x)
		return flat
	'''
