# -*- coding: utf-8 -*-

import re

class Phonemes(object):
	PALATALIZABLES = ["c","dz","n","s","z"]
	DIGRAPHS = ["ch","cz","drz","dz","dzi","rz","sz"]
	VOWELS = ["a","on","e","en","i","o","u","y"]
	POLISH_LETTERS = {
		u"ą":	"on",
		u"ć":	"ci",
		u"ę":	"en",
		u"ł":	"ll",
		u"ń":	"ni",
		u"ó":	"u",
		u"ś":	"si",
		u"ź":	"zi",
		u"ż":	"rz"}
	VOICELESS_EQUIVALENTS = {
		"b":	"p",
		"d":	"t",
		"w":	"f",
		"g":	"k",
		"z":	"s",
		"rz":	"sz",
		"drz":	"cz",
		"zi":	"si",
		"dz":	"c",
		"dzi":	"ci"}
	VOICED_EQUIVALENTS = {
		"p":	"b",
		"t":	"d",
		"f":	"w",
		"k":	"g",
		"s":	"z",
		"sz":	"rz",
		"cz":	"drz",
		"si":	"zi",
		"c":	"dz",
		"ci":	"dzi"}
	@classmethod
	def line_to_phonemes(cls, line):
		line = line.lower()
		phonemes = []
		words = line.split()
		for word in words:
			phonemes += cls.word_to_phonemes(word)
			phonemes += [" "]

		if(len(phonemes)>1):
			del phonemes[len(phonemes)-1]
		return phonemes

	@classmethod
	def word_to_phonemes(cls, word):
		word = word.lower()
		phonemes = []
		if len(word) > 0:
			for i in range(0,len(word)):
				letter = word[i:i+1]
				if cls.POLISH_LETTERS.has_key(letter):
					phonemes += [cls.POLISH_LETTERS[letter]]
				else:
					if(letter == u"x"):
						phonemes += ["k", "s"]
					else:
						phonemes += [letter.encode("ascii","ignore")]
			cls.connect_digraphs(phonemes);
			cls.palatalize(phonemes);
			cls.lengthen_i(phonemes);
			cls.unnasalize_vowels(phonemes);
			cls.split_nosal_vowels(phonemes);
			cls.fix_last(phonemes);
			cls.backward_voiceless(phonemes);
			cls.forward_voiceless(phonemes);
			cls.backward_voiced(phonemes);
			cls.fix_letter_u(phonemes);
		return phonemes

	@classmethod
	def connect_digraphs(cls, phonemes):
		i = len(phonemes)-1
		while i > 0:
			if cls.is_digraph(phonemes[i-1], phonemes[i]):
				phonemes[i-1] = phonemes[i-1]+phonemes[i]
				if(phonemes[i-1] == "ch"):
					phonemes[i-1] = "h"
				del phonemes[i]
			i-=1

	@classmethod
	def palatalize(cls, phonemes):
		i = len(phonemes)-1
		while i > 0:
			if phonemes[i]=="i" and cls.is_palatalizable(phonemes[i-1]):
				phonemes[i-1] = phonemes[i-1]+"i"
				if i+1 < len(phonemes) and cls.is_vowel(phonemes[i+1]):
					del phonemes[i]
				i-=1
			i-=1

	@classmethod
	def lengthen_i(cls, phonemes):
		i = 0
		while i<len(phonemes)-1:
			if phonemes[i]=="i" and cls.is_vowel(phonemes[i+1]):
				phonemes[i] = "j"
				i+=1;
			i+=1

	@classmethod
	def unnasalize_vowels(cls, phonemes):
		i = 0
		while i<len(phonemes)-1:
			if phonemes[i] in ["on", "en"] and phonemes[i+1] in ["l", "ll"]:
				phonemes[i] = phonemes[i][0:1]
				i+=1
			i+=1

	@classmethod
	def fix_last(cls, phonemes):
		if len(phonemes)>1:
			if cls.VOICELESS_EQUIVALENTS.has_key(phonemes[-1]):
				phonemes[-1] = cls.VOICELESS_EQUIVALENTS[phonemes[-1]]
			if phonemes[-1] == "en":
				phonemes[-1] = "e"
		if len(phonemes)>2:
			if phonemes[-1] == "i" and (phonemes[-2] in ["i", "j"]):
				del phonemes[-1]
				phonemes[-1] = "i"


	@classmethod
	def backward_voiceless(cls, phonemes):
		i = 0
		while i < len(phonemes)-1:
			if cls.VOICELESS_EQUIVALENTS.has_key(phonemes[i]) and cls.VOICED_EQUIVALENTS.has_key(phonemes[i+1]):
				phonemes[i] = cls.VOICELESS_EQUIVALENTS[phonemes[i]]
				i+=1
			i+=1

	@classmethod
	def forward_voiceless(cls, phonemes):
		i = len(phonemes)-1
		while i > 0:
			if cls.VOICED_EQUIVALENTS.has_key(phonemes[i-1]) and phonemes[i] in ["w", "rz"]:
				phonemes[i] = cls.VOICELESS_EQUIVALENTS[phonemes[i]]
				i-=1
			i-=1

	@classmethod
	def backward_voiced(cls, phonemes):
		i = 0
		while i < len(phonemes)-1:
			if cls.VOICED_EQUIVALENTS.has_key(phonemes[i]) and cls.VOICELESS_EQUIVALENTS.has_key(phonemes[i+1]):
				phonemes[i] = cls.VOICED_EQUIVALENTS[phonemes[i]]
				i+=1
			i+=1

	NOSAL_VOWEL_SPLITTERS = ["t","d","b","p","ci","dzi","dz","c"]
	@classmethod
	def split_nosal_vowels(cls, phonemes):
		i = 0
		while i<len(phonemes)-1:
			if phonemes[i] in ["on","en"] and phonemes[i+1] in cls.NOSAL_VOWEL_SPLITTERS:
				if phonemes[i+1] in ["b", "p"]:
					phonemes.insert(i+1, "m");
				else:
					if cls.is_palatalized(phonemes[i+1]):
						phonemes.insert(i+1, "ni")
					else:
						phonemes.insert(i+1, "n")


				phonemes[i] = phonemes[i][0:1]
				i+=2
			i+=1

	PREFIXES_WITH_AU = ["nau","zau","prau", "unau", "pozau","nienau","niezau","nieprau", "nieunau", "niepozau"]
	@classmethod
	def has_au_prefix_exception(cls, word):
		for prefix in cls.PREFIXES_WITH_AU:
			if re.match(prefix, word):
				# exceptions:
				#	.*au.o.*
				#	.*au.$
				return not (len(word)==len(prefix)+1) # or (len(word)>len(prefix)+1 and word[len(prefix)+1:len(prefix)+2]=="o"))
		return False

	PREFIXES_WITH_EU = ["przeu","nieprzeu"]
	@classmethod
	def has_eu_prefix_exception(cls, word):
		for prefix in cls.PREFIXES_WITH_EU:
			if re.match(prefix, word):
				return True
		return False

	# exceptions:
	#	.*eusz.*
	#	.*eusi.*
	#	.*euj.*
	#	.*eu.$
	#	.*aurk.*
	EU_EXCEPTIONAL_SUCCESSORS = ["sz","si","j"]
	@classmethod
	def fix_letter_u(cls, phonemes):
		word = "".join(phonemes)
		skip_first = cls.has_au_prefix_exception(word) or cls.has_eu_prefix_exception(word);
		for i in range(1,len(phonemes)):
			if phonemes[i]=="u" and phonemes[i-1] in ["a","e"]:
				if skip_first:
					skip_first = False
					continue
				if phonemes[i-1]=="e":
					if i+2 == len(phonemes):
						break
					if i+1 < len(phonemes) and phonemes[i+1] in cls.EU_EXCEPTIONAL_SUCCESSORS:
						continue

				else:
					if i+2 < len(phonemes) and phonemes[i+1]+phonemes[i+2]=="rk":
						continue
				phonemes[i] = "ll"

	@classmethod
	def is_digraph(cls, l1, l2):
		d = l1+l2
		return d in cls.DIGRAPHS

	@classmethod
	def is_palatalizable(cls, l):
		return l in cls.PALATALIZABLES

	@classmethod
	def is_palatalized(cls, l):
		return re.match("[a-z]+i$", l)

	@classmethod
	def is_vowel(cls, l):
		return l in cls.VOWELS

	@classmethod
	def is_consonant(cls, l):
		return not cls.is_vowel(l)

	@classmethod
	def is_phoneme(cls, l):
		return re.match("[a-z]{1,3}$", l)


