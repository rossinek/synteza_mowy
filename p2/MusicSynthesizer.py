import re
import sys

from Instrument import Instrument
from ..p1 import WaveEditor
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
			for line in melody_file.readlines():
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
					instruments[-1].add_sound(line_s[0], line_s[1])
					nsounds += 1
				else:
					raise ValueError('Wrong melody file syntax')
		except ValueError:
			melody_file.close()
			print "\nError reading melody file"
			return
				
		print "Writing melodies for each instument..."
		# setup progressbar
		nprocessed_sounds = 0
		progressbar_width = 50
		sys.stdout.write("%3d%% [%s]" % (0, (" " * progressbar_width)))
		sys.stdout.flush()
		
		melodies = []

		for inst in instruments:
			files_list = [f for f in listdir(WAVES_PATH)]
			samp = next(x for x in files_list if re.match(inst.name+".*.wav", x))
			melody = WaveEditor(WAVES_PATH+"/"+samp)
			melody.crop(0, 0)

			i_sounds = inst.get_sounds()
			i_melody = inst.get_melody()

			for (sound, length) in i_melody:
				duration = float(length)*tempo_factor*4.0
				if(sound=="p"):
					melody.append(melody.gen_silence(duration))
				else:
					se = copy.deepcopy(i_sounds[sound])
					duration_difference = duration*se.getframerate() - se.getnvalues()
					if duration_difference < 0:
						se.crop(0, duration)
						se.fade_out(0.20)
					else:
						se.append(se.gen_silence(duration_difference/se.getframerate()))
					melody.append(se.getbytes())
				
				# progressbar update
				nprocessed_sounds += 1
				sys.stdout.write("\b" * (progressbar_width+7)) # return to start of line, after '['
				percentage = (nprocessed_sounds*100.0)/nsounds
				processed_width = int((float(nprocessed_sounds)/nsounds)*progressbar_width)
				sys.stdout.write("%3d%% [%s]" % (int(percentage), (("#"*processed_width)+(" "*(progressbar_width-processed_width)))))
				sys.stdout.flush()
			melodies.append((melody, inst.volume))

		print "\nAdding and normalizing waves..."
		song = WaveEditor.add_waves(melodies)
		print "Done!"
		print "Now listen and chill out..."
		song.save("synteza_mowy/p2/output.wav")
		WaveEditor.play("synteza_mowy/p2/output.wav")
	