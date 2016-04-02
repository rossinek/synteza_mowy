from SoundEditor import SoundEditor

class Instrument(object):
	
	def __init__(self, name, volume):
		self.name = name
		self.volume = volume
		self.sounds = {}
		self.melody = []
		self.params = None

	def add_sound(self, sound, duration, progressbar=None):
		if sound != "p" and (not self.sounds.has_key(sound)):
			self.sounds[sound] = SoundEditor(self.name, sound[0:-1], int(sound[-1]), progressbar)
			if self.params==None:
				self.params = self.sounds[sound].getparams()
		self.melody.append((sound, duration))

	def get_melody(self):
		return self.melody

	def get_sounds(self):
		return self.sounds

	def getparams(self):
		return self.params