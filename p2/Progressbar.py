import sys

class Progressbar(object):

	def __init__(self, width, maximum, progress=0):
		self.width = width
		self.maximum = maximum
		self.progress = progress
		self.min_diff = (maximum/100)
		self.update()

	def update(self, progress=None):
		if progress==None:
			progress = self.progress
		elif abs(self.progress-progress) < self.min_diff:
			return
		else:
			self.progress = progress

		percentage = int((100*self.progress)/self.maximum)
		done = int((self.width*self.progress)/self.maximum)
		if done > self.width:
			done = self.width
		sys.stdout.write('%3d%% [%s]' % (int(percentage), (('#'*done)+(' '*(self.width-done)))))
		sys.stdout.flush()
		sys.stdout.write("\b" * (self.width+7))

	def message(self, msg):
		rest = (self.width+7) - len(msg)
		if rest < 0:
			rest = 0
		sys.stdout.write(msg + (' '*rest) + '\n')
		sys.stdout.flush()
		self.update()

	def update_add1(self):
		self.progress = self.progress+1
		percentage = int((100*self.progress)/self.maximum)
		done = int((self.width*self.progress)/self.maximum)
		if done > self.width:
			done = self.width
		sys.stdout.write('%3d%% [%s]' % (int(percentage), (('#'*done)+(' '*(self.width-done)))))
		sys.stdout.flush()
		sys.stdout.write('\b' * (self.width+7))

	def finish(self, msg='Done!'):
		rest = (self.width+7) - len(msg)
		if rest < 0:
			rest = 0
		sys.stdout.write(msg + (' '*rest) + '\n')
		sys.stdout.flush()
