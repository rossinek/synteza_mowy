import math
import numpy
import copy

from ..p1.WaveEditor import WaveEditor
from Progressbar import Progressbar

def rms(a):
	return math.sqrt(sum(map(lambda x:x*x, a))/float(len(a)))

class WaveAnalyzer(WaveEditor):
		
	def __init__(self, path):
		WaveEditor.__init__(self, path)

	def split(self, nparts):
		bg_samp = self.values[:(self.getframerate()/15)*self.getnchannels()]
		mean = float(sum(bg_samp))/len(bg_samp)
		stdd = numpy.std(bg_samp)
		threshold = 1.3
		is_voice = [((abs(v)-mean)/stdd>threshold) for v in self.values]
		parts = self.count_parts(is_voice, nparts)
		print len(parts)

		we = WaveEditor(self.getparams())
		for i,p in enumerate(parts):
			if i==0:
				sb = 0
			else:
				sb = parts[i-1][1]
			we.concat(we.gen_silence(float(p[0]-sb)/self.getframerate()))
			we.concat(self.values[p[0]:p[1]])
		return we

	def count_parts(self, is_voice, nparts):
		parts = []
		n = 767

		sums = map(sum, self.chunks(is_voice, n))

		parts = []
		progressbar = Progressbar(50, len(sums))

		for i,s in enumerate(sums):
			progressbar.update(i)
			if s>n/2:
				if len(parts)==0 or len(parts[-1])==2:
					parts.append([i*n])
			elif len(parts)>0 and len(parts[-1])<2:
				parts[-1].append(min((i+1)*n, len(is_voice)))

		if len(parts)>0 and len(parts[-1])<2:
			parts[-1].append(len(is_voice))
		
		if len(parts) > nparts:
			diff = len(parts) - nparts
			parts_rms = map(lambda (i,x): x+[(self.rms_from(x[0],x[1]-x[0])), i], enumerate(parts))
			parts_rms = sorted(parts_rms, key=lambda x:x[2])
			waste = parts_rms[:diff]
			waste_rms = map(lambda x: x[2], waste)
			waste_rms_mean = float(sum(waste_rms[:len(waste)/2]))/(len(waste)/2)
			waste_rms_stdd = numpy.std(waste_rms[:len(waste)/2])
			t = 1.2
			voice_parts = parts_rms[diff:]
			parts = map(lambda x: x+[True], voice_parts) + map(lambda x: x+[False], waste)
			parts = sorted(parts, key=lambda x: x[3])
			parts_is_voice = map(lambda x: x[4], parts)
			for w in waste:
				try:
					next_voice_index=parts_is_voice[w[3]:].index(True)+w[3]
					dist_to_next_voice = parts[next_voice_index][0]-w[1]
				except ValueError:
					dist_to_next_voice = float('inf')
				try:
					prev_voice_index=w[3]-parts_is_voice[w[3]:][::-1].index(True)
					dist_to_prev_voice = w[0]-parts[prev_voice_index][1]
				except ValueError:
					if dist_to_prev_voice==float('inf'):
						break
				dist_to_voice = min(dist_to_prev_voice, dist_to_next_voice)
				if (
						(
							(w[2]-waste_rms_mean)/waste_rms_stdd > 16*t and
							dist_to_voice<=n*3
						) or
						(
							(w[2]-waste_rms_mean)/waste_rms_stdd > t and 
							dist_to_next_voice<=n
						)
					):
					voice_parts.append(w)
			parts = sorted(voice_parts, key=lambda x: x[0])

			#concat some parts
			holes = map(lambda (i,x): [x[1],parts[i+1][0]], enumerate(parts[:-1]))
			diff = len(holes)-(nparts-1)
			if diff>0:
				holes.sort(key=lambda x: x[1]-x[0])
				holes = holes[diff:]
				holes.sort(key=lambda x: x[0])
				c_parts = [ [parts[0][0], holes[0][0]] ]
				c_parts += map(lambda (i,x): [x[1], holes[i+1][0]], enumerate(holes[:-1]))
				c_parts += [ [holes[-1][1],parts[-1][1]] ]
				parts = c_parts
		progressbar.finish()

		return parts

	def chunks(self, l, n):
		for i in xrange(0, len(l), n):
			yield l[i:i+n]
	
	def rms_from(self, begin, n=16):
		offset = begin*self.getnchannels()
		return rms(self.values[offset:offset+n*self.getnchannels()])
