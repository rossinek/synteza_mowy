import wave
import struct
import copy

from ..p1.WaveEditor import WaveEditor

class SoundEditor(WaveEditor):
	
	SOUNDS = ["c","c#","d","d#","e","f","f#","g", "g#","a","a#","b"]
	INSTRUMENT_PATH = "synteza_mowy/p2/instruments/"
	
	def __init__(self, instrument, sound, octave, progressbar=None):
		difference = -1
		wav = None
		nearest_sound = None
		while wav is None:
			difference += 1
			for sign in [-1, 1]:
				nearest_sound = [(self.SOUNDS.index(sound)+(sign*difference))%12, octave+(self.SOUNDS.index(sound)+(sign*difference))/12]
				if nearest_sound[1] < 0:
					continue
				for suf in ['', '_gen']:
					try:
						path = self.INSTRUMENT_PATH+instrument+"-"+self.SOUNDS[nearest_sound[0]]+str(nearest_sound[1])+suf+'.wav'
						wav = wave.open(path, "r")
					except:
						if difference==0 and sign<0:
							msg = "Searching for nearest sound for "+instrument+"'s "+sound+str(octave)
							if progressbar:
								progressbar.message(msg)
							else:
								print msg
						wav = None
					if not (wav is None):
						difference = sign*difference
						break
		wav.close()
		WaveEditor.__init__(self, path)
		
		if difference != 0:
			msg = "Tuning up "+instrument+"'s "+self.SOUNDS[nearest_sound[0]]+str(nearest_sound[1])+" to "+sound+str(octave)+"..."
			if progressbar:
				progressbar.message(msg)
			else:
				print msg
			self.tune(difference)

		self.save(self.INSTRUMENT_PATH+instrument+"-"+sound+str(octave)+"_gen.wav")

	def tune(self, difference):
		new_values = []
		nold_values = self.getnvalues()
		nnew_values = int(nold_values*pow(2.0, difference/12.0))
		
		for i in range(0, nnew_values):
			pos = float(i*nold_values)/float(nnew_values)
			if pos >= float(nold_values):
				pos = float(nold_values)

			for c in range(0, self.getnchannels()):
				v0 = self[int(pos), c]
				if int(pos)+1 >= nold_values:
					v1 = v0
				else:
					v1 = self[int(pos)+1, c]
				v = float(v0) + float(pos-float(int(pos)))*float(v1-v0)
				new_values.append(v)

		self.values = new_values

	def clone_we(self):
		we = WaveEditor(self.getparams())
		we.values = copy.copy(self.values)
		return we


