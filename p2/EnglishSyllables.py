
from EnglishPhonemes import EnglishPhonemes

import re

class EnglishSyllables(object):
	
	def __init__(self):
		self.validation_data = None

		self.nlearned = 0
		self.part_prob = {}
		self.context_part_prob = {}

		self.part_prefix_prob = {}
		self.part_suffix_prob = {}
		self.context_part_prefix_prob = {}
		self.context_part_suffix_prob = {}

	def separate_syllables(self, _phonemes):
		phonemes = re.sub('\d', '', _phonemes)
		parts = re.split('('+EnglishPhonemes.get_vowel_pattern()+')', phonemes)
		new_phonemes = parts[0]
		for i in range(1, len(parts)-1):
			if not EnglishPhonemes.is_vowel(parts[i]):
				new_phonemes += self.separate_sequence(parts[i], parts[i-1], parts[i+1])
			else:
				new_phonemes += parts[i]
		new_phonemes += parts[-1]
		return new_phonemes

	def separate_sequence(self, _phonemes, vowel_before, vowel_after):
		phonemes = _phonemes.split()
		sequence = ''.join(phonemes)
		context_sequence = vowel_before+sequence+vowel_after
		if self.context_part_prob.has_key(context_sequence):
			probs = self.context_part_prob[context_sequence]
			partition_index = max(xrange(len(probs)),key=probs.__getitem__)
		elif self.part_prob.has_key(sequence):
			probs = self.part_prob[sequence]
			partition_index = max(xrange(len(probs)),key=probs.__getitem__)
		else:
			pre_probs = [0]*(len(phonemes)+1)
			suf_probs = [0]*(len(phonemes)+1)
			context_pre_probs = [0]*(len(phonemes)+1)
			context_suf_probs = [0]*(len(phonemes)+1)
			for i in range(0, len(phonemes)+1):
				seq_prefix = ''.join(phonemes[:i])
				seq_suffix = ''.join(phonemes[i:])
				context_seq_prefix = vowel_before + ''.join(phonemes[:i])
				context_seq_suffix = ''.join(phonemes[i:]) + vowel_after
				if(self.part_prefix_prob.has_key(seq_prefix)):
					pre_probs[i] = self.part_prefix_prob[seq_prefix]

				if(self.part_suffix_prob.has_key(seq_suffix)):
					suf_probs[i] = self.part_suffix_prob[seq_suffix]

				if(self.context_part_prefix_prob.has_key(context_seq_prefix)):
					context_pre_probs[i] = self.context_part_prefix_prob[context_seq_prefix]

				if(self.context_part_suffix_prob.has_key(context_seq_suffix)):
					context_suf_probs[i] = self.context_part_suffix_prob[context_seq_suffix]

			if max([max(context_pre_probs),max(context_suf_probs)]) > 0:
				if max(context_pre_probs) > max(context_suf_probs):
					partition_index = max(xrange(len(context_pre_probs)),key=context_pre_probs.__getitem__)
				else:
					partition_index = max(xrange(len(context_suf_probs)),key=context_suf_probs.__getitem__)
			elif max([max(pre_probs),max(suf_probs)]) > 0:
				if max(pre_probs) > max(suf_probs):
					print pre_probs
					partition_index = max(xrange(len(pre_probs)),key=pre_probs.__getitem__)
				else:
					partition_index = max(xrange(len(suf_probs)),key=suf_probs.__getitem__)
			else:
				partition_index = 0
		

		phonemes.insert(partition_index, '-')
		return ' ' + ' '.join(phonemes) + ' '

	def validate(self, validate_set_path):
		total = 0
		accepted = 0

		dict_file = open(validate_set_path, "r")

		line = dict_file.readline()
		while line != '':
			if not re.match('\n|##', line):
				total += 1
				word = line.split(' ', 1)[1]
				word = re.sub('\d', '', word)
				clean_world = word.replace('- ', '')
				res = self.separate_syllables(clean_world)
				if res.split() == word.split():
					accepted += 1

			line = dict_file.readline()

		return (accepted, total)

	def learn(self, learning_set_path):
		dict_file = open(learning_set_path, "r")

		line = dict_file.readline()
		while line != '':
			if not re.match('\n|##', line):
				word = line.split(' ', 1)[1]
				word = re.sub('\d', '', word)
				parts = re.split('('+EnglishPhonemes.get_vowel_pattern()+')', word)
				for i in range(1,len(parts)-1):
					if '-' in parts[i] and  EnglishPhonemes.is_vowel(parts[i-1]) and EnglishPhonemes.is_vowel(parts[i+1]):
						self.learn_partition(parts[i], parts[i-1], parts[i+1])
				if len(parts) > 1:
					if len(parts[0].split())>0 and (not EnglishPhonemes.is_vowel(parts[0])) and EnglishPhonemes.is_vowel(parts[1]):
						suffix_seq = ''.join(parts[0].split())
						self.learn_suffix(suffix_seq, parts[1])
						
					if len(parts[-1].split())>0 and (not EnglishPhonemes.is_vowel(parts[-1])) and EnglishPhonemes.is_vowel(parts[-2]):
						prefix_seq = ''.join(parts[-1].split())
						self.learn_prefix(prefix_seq, parts[-2])
				self.nlearned += 1
			line = dict_file.readline()

		learned = True

	def learn_partition(self, _phonemes, vowel_before, vowel_after):
		phonemes = _phonemes.split()
		partition_index = phonemes.index('-')
		del phonemes[partition_index]

		sequence = ''.join(phonemes)
		if not self.part_prob.has_key(sequence):
			self.part_prob[sequence] = [0] * (len(sequence)+1)
		self.part_prob[sequence][partition_index] += 1

		context_sequence = vowel_before+sequence+vowel_after
		if not self.context_part_prob.has_key(context_sequence):
			self.context_part_prob[context_sequence]  = [0] * (len(sequence)+1)
		self.context_part_prob[context_sequence][partition_index] += 1

		seq_prefix = ''.join(phonemes[:partition_index])
		seq_suffix = ''.join(phonemes[partition_index:])

		self.learn_prefix(seq_prefix, vowel_before)
		self.learn_suffix(seq_suffix, vowel_after)

	def learn_prefix(self, seq_prefix, vowel_before):
		if not self.part_prefix_prob.has_key(seq_prefix):
			self.part_prefix_prob[seq_prefix] = 0
		self.part_prefix_prob[seq_prefix] += 1
		
		if vowel_before:
			context_seq_prefix = vowel_before+seq_prefix
			if not self.context_part_prefix_prob.has_key(context_seq_prefix):
				self.context_part_prefix_prob[context_seq_prefix] = 0
			self.context_part_prefix_prob[context_seq_prefix] += 1

	def learn_suffix(self, seq_suffix, vowel_after):

		if not self.part_suffix_prob.has_key(seq_suffix):
			self.part_suffix_prob[seq_suffix] = 0
		self.part_suffix_prob[seq_suffix] += 1
		
		if vowel_after:
			context_seq_suffix = seq_suffix+vowel_after
			if not self.context_part_suffix_prob.has_key(context_seq_suffix):
				self.context_part_suffix_prob[context_seq_suffix] = 0
			self.context_part_suffix_prob[context_seq_suffix] += 1
 