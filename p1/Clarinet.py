import re

from WaveEditor import WaveEditor

class Clarinet(object):

	@classmethod
	def play(cls, path_melody):
		melody_file = open(path_melody, "r")
		line = melody_file.readline()
		while not re.match("TEMPO", line):
			if line == '':
				print "No TEMPO in file"
				melody_file.close()
				return
			line = melody_file.readline()

		print line
		tempo = int(re.findall("\d+", line)[0])
		tempo_factor = 60.0/tempo
		melody = WaveEditor("synteza_mowy/p1/klarnet/c.wav")
		melody.crop(0, 0)

		line = melody_file.readline()
		while line != '':
			if not re.match("\n|#", line):
				el = line.split()
				sound = el[0]
				duration = float(el[1])*tempo_factor*4.0
				
				if(sound=="p"):
					melody.append(melody.gen_silence(duration))
				else:
					we = WaveEditor("synteza_mowy/p1/klarnet/"+sound+".wav")
					duration_difference = duration*we.getframerate() - we.getnvalues()
					if duration_difference < 0:
						we.crop(0, duration)
						we.fade_out(0.1)
					else:
						we.append(we.gen_silence(duration_difference))
					melody.append(we.getbytes())
			line = melody_file.readline()
	
		melody_file.close()
		melody.save("synteza_mowy/p1/output.wav")
		WaveEditor.play("synteza_mowy/p1/output.wav")
	