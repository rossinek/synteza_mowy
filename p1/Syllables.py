
from Phonemes import Phonemes

class Syllables(object):
	
	@classmethod
	def separate_syllables(cls, phonemes):
		last_vowel = -1
		i = 0
		while i < len(phonemes):
			if not Phonemes.is_phoneme(phonemes[i]):
				last_vowel = -1
			elif Phonemes.is_vowel(phonemes[i]):
				if(last_vowel >= 0):
					if i-last_vowel > 2:
						phonemes.insert(last_vowel+2, "|")
					else:
						phonemes.insert(last_vowel+1, "|")
					i+=1
				last_vowel = i
			i+=1
		return phonemes

	@classmethod
	def count_syllables(cls, phonemes, offset):
		# assuming that phonemes[i] is phoneme
		syllables_num = 1
		i = offset+1
		while i < len(phonemes):
			if phonemes[i] == "|":
				syllables_num += 1
			elif not Phonemes.is_phoneme(phonemes[i]):
				break
			i+=1
		return syllables_num				