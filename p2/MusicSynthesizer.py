import re
import sys

from Instrument import Instrument
from Progressbar import Progressbar
from ..p1.WaveEditor import WaveEditor
import copy
from os import listdir

WAVES_PATH = "synteza_mowy/p2/instruments"

class MusicSynthesizer(object):

	@classmethod
	def play(cls, path_melody):
		melody_file = open(path_melody, "r")
		
		print "Reading melody file and tuning up sounds..."

		# length of all melodies for progressbar
		nsounds = 0

		try:
			tempo_factor = None;
			instruments = []
			flines = melody_file.readlines()

			progressbar = Progressbar(50, len(flines))

			for line in flines:
				line_s = line.split()
				if re.match("$|#", line):
					continue
				if (tempo_factor is None) and (line_s[0] == "TEMPO"):
					tempo = int(re.findall("\d+", line)[0])
					tempo_factor = 60.0/tempo
				elif line_s[0] == "inst" and len(line_s) == 3:
					inst = Instrument(line_s[1], int(line_s[2]))
					instruments.append(inst)
				elif re.match("[a-g]#?\d|p", line_s[0]):
					instruments[-1].add_sound(line_s[0], line_s[1], progressbar)
					nsounds += 1
				else:
					raise ValueError('Wrong melody file syntax')
				progressbar.update_add1()
			
			progressbar.finish()

		except ValueError:
			melody_file.close()
			print "\nError reading melody file"
			return

		print "Writing melodies for each instument..."

		progressbar = Progressbar(50, nsounds)

		melodies = []
		for inst in instruments:
			melody = WaveEditor(inst.getparams())
			i_sounds = inst.get_sounds()
			i_melody = inst.get_melody()

			for (sound, length) in i_melody:
				duration = float(length)*tempo_factor*4.0
				if(sound=="p"):
					melody.concat(melody.gen_silence(duration))
				else:
					we = i_sounds[sound].clone_we()

					duration_difference = duration*we.getframerate() - we.getnvalues()
					if duration_difference < 0:
						we.crop(0, duration)
						we.fade_out(0.1)
					else:
						we.concat(we.gen_silence(duration_difference/we.getframerate()))
					melody.concat(we.getvalues())

				progressbar.update_add1()
			melodies.append((melody, inst.volume))

		progressbar.finish()


		song = WaveEditor.add_waves(melodies, True)
		print "Now listen and chill out..."
		song.save("synteza_mowy/p2/output.wav")
		WaveEditor.play("synteza_mowy/p2/output.wav")
	