import wave
import math
import struct
import subprocess
import thread
import sys

from Phonemes import Phonemes
from Syllables import Syllables

class SimpleSynthesizer(object):

	SPACERS = {
		" ": 0.2,
		",": 0.4,
		".": 0.6}

	ACCENT_FACTOR = 2.0

	PHONEMES_PATHS = ["fonemy2016", "fonemy_bodek", "dzwieki1"]

	@classmethod
	def synthesize(cls, phonemes, phonemes_set):
		phonemes_path = cls.PHONEMES_PATHS[phonemes_set%3]
		output_path = "output.wav"
		cls._synthesize(phonemes, phonemes_path, output_path)
		try:
			thread.start_new_thread(cls.play, (output_path,))
		except:
			print "Error: unable to start thread"

	@classmethod
	def _synthesize(cls, phonemes, phonemes_path, output_path):
		wave_output = wave.open(output_path, "w")
		wave_output.setparams(cls.wave_getparams(phonemes_path))

		phonemes_bytes = []

		syllables_num = -1
		accent_on = -1
		i = 0
		while i < len(phonemes):
			p = phonemes[i]
			if Phonemes.is_phoneme(p):
				# set accent
				if syllables_num < 0:
					syllables_num = 0
					accent_on = Syllables.count_syllables(phonemes, i)
					if accent_on == 1:
						accent_on -= 1
					else:
						accent_on -= 2

				p_wav = wave.open(cls.phoneme_wav_path(p, phonemes_path), "r")
				p_bytes = p_wav.readframes(p_wav.getnframes())
				p_wav.close()
				if syllables_num == accent_on:
					phonemes_bytes.append(p_bytes)	
				else:
					phonemes_bytes.append(cls.set_volume(p_bytes, 1.0/cls.ACCENT_FACTOR))
			elif p == "|":
				syllables_num += 1
			else:
				syllables_num = accent_on = -1
				if cls.SPACERS.has_key(p):
					phonemes_bytes.append(cls.gen_silence(cls.SPACERS[p], phonemes_path))
			i+=1

		wave_output.writeframes("".join(phonemes_bytes))
		wave_output.close()

	@classmethod
	def phoneme_wav_path(cls, phoneme, phonemes_path):
		return phonemes_path+"/"+phoneme+".wav"

	@classmethod
	def wave_getparams(phonemes_pathcls, phonemes_path):
		s = wave.open(phonemes_path+"/a.wav", "rb")
		params = s.getparams()
		s.close
		return params

	@classmethod
	def gen_silence(cls, seconds, phonemes_path):
		(_, _, framerate, _, _, _) = cls.wave_getparams(phonemes_path)
		values = []
		for i in range(0, int(framerate*seconds)):
			values.append(struct.pack("h", 0))
		return "".join(values)

	@classmethod
	def set_volume(cls, values, factor):
		new_values = []
		for i in range(0, len(values)/2):
			(v,) = struct.unpack("h", values[2*i:2*i+2])
			new_values.append(struct.pack("h", int(v)*factor))
		return "".join(new_values)

	@classmethod
	def play(cls, path):
		if sys.platform == "darwin":
			subprocess.call(["afplay", path])
		elif sys.platform == "linux2":
			subprocess.call(["aplay", path, "-q"])
