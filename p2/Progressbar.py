import re
import sys

class Progressbar(object):

	def __init__(self, width, maximum, progress=0):
		self.width = width
		self.maximum = maximum
		self.progress = progress
		self.min_diff = (maximum/100)
		self.update(progress)

	def update(self, progress):
		if abs(self.progress-progress) < self.min_diff:
			return

		self.progress = progress

		percentage = int((100*self.progress)/self.maximum)
		done = int((self.width*self.progress)/self.maximum)
		if done > self.width:
			done = self.width
		sys.stdout.write("%3d%% [%s]" % (int(percentage), (("#"*done)+(" "*(self.width-done)))))
		sys.stdout.flush()
		sys.stdout.write("\b" * (self.width+7))

	def update_add1(self):
		self.progress = self.progress+1
		percentage = int((100*self.progress)/self.maximum)
		done = int((self.width*self.progress)/self.maximum)
		if done > self.width:
			done = self.width
		sys.stdout.write("%3d%% [%s]" % (int(percentage), (("#"*done)+(" "*(self.width-done)))))
		sys.stdout.flush()
		sys.stdout.write("\b" * (self.width+7))

	def finish(self, msg="Done!"):
		print msg + ((self.width+7-len(msg))*" ")
	