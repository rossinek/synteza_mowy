
class EnglishPhonemes(object):
	VOWELS = ["AA","AE","AH","AO","AW","AY","EH","ER","EY","IH","IY","OW","OY","UH","UW"]
	VOWELS_PATTERN = "[AEIOU]."

	@classmethod
	def is_vowel(cls, l):
		return l in cls.VOWELS

	@classmethod
	def is_consonant(cls, l):
		return not cls.is_vowel(l)

	@classmethod
	def get_vowel_pattern(cls):
		return cls.VOWELS_PATTERN
