import wave
import struct
import sys
import subprocess

from ..p1.WaveEditor import WaveEditor

class SoundEditor(WaveEditor):
	
	SOUNDS = ["c","c#","d","d#","e","f","f#","g", "g#","a","a#","b"]
	INSTRUMENT_PATH = "synteza_mowy/p2/instruments/"
	
	def __init__(self, instrument, sound, octave):
		difference = -1
		wav = None
		nearest_sound = None
		while wav is None:
			difference += 1
			for sign in [-1, 1]:
				nearest_sound = [(self.SOUNDS.index(sound)+(sign*difference))%12, octave+(self.SOUNDS.index(sound)+(sign*difference))/12]
				if nearest_sound[1] < 0:
					continue
				try:
					path = self.INSTRUMENT_PATH+instrument+"-"+self.SOUNDS[nearest_sound[0]]+str(nearest_sound[1])+".wav"
					wav = wave.open(path, "r")
				except:
					if difference==0 and sign<0:
						print "Searching for nearest sound for "+instrument+"'s "+sound+str(octave)
					wav = None
				if not (wav is None):
					difference = sign*difference
					break
		wav.close()
		WaveEditor.__init__(self, path)
		
		if difference != 0:
			print "Tuning up "+instrument+"'s "+self.SOUNDS[nearest_sound[0]]+str(nearest_sound[1])+" to "+sound+str(octave)+"..."
			self.tune(difference)

		self.save(self.INSTRUMENT_PATH+instrument+"-"+sound+str(octave)+".wav")

	def tune(self, difference):
		new_bytes = ''
		old_nvalues = self.getnvalues()/2
		new_nvalues = int(old_nvalues*pow(2.0, difference/12.0))
		
		for i in range(0, new_nvalues):
			pos = float(i*old_nvalues)/float(new_nvalues)
			if pos >= float(old_nvalues):
				pos = float(old_nvalues)

			for channel in [0, 1]:
				(v0,) = struct.unpack("h", self.bytes[4*int(pos)+channel*2:4*int(pos)+channel*2+2])
				if int(pos)+2 >= old_nvalues:
					v1 = v0
				else:
					(v1,) = struct.unpack("h", self.bytes[4*int(pos)+4+channel*2:4*int(pos)+6+channel*2])
			
				v = float(v0) + float(pos-float(int(pos)))*float(v1-v0)
				new_bytes += struct.pack("h", int(v))

		self.bytes = new_bytes
