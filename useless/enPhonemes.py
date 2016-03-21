# -*- coding: utf-8 -*-

import re
import os
import subprocess

class EnPhonemes(object):
	SIMPLE_TRANSLATE = {
		"a":	"ao",
		"b":	"b",
		"c":	"ts",
		"ch":	"h",
		"ci":	"ci",
		"cz":	"tch",
		"d":	"d",
		"drz":	"j",
		"dz":	"dz",
		"dzi":	"dzee",
		"e":	"e",
		"en":	"en",
		"f":	"f",
		"g":	"g",
		"h":	"h",
		"i":	"ee",
		"j":	"y",
		"k":	"ck",
		"l":	"l",
		"ll":	"w",
		"m":	"m",
		"n":	"n",
		"ni":	"n",
		"o":	"o",
		"on":	"oun",
		"p":	"p",
		"r":	"r",
		"rz":	"j",
		"s":	"ts",
		"si":	"tsi",
		"sz":	"sh",
		"t":	"t",
		"u":	"oo",
		"w":	"the",
		"y":	"ie",
		"z":	"zz",
		"zi":	"zee"}

	@classmethod
	def simple_translator(cls, phonemes):
		new_phonemes = []
		for p in phonemes:
			if cls.SIMPLE_TRANSLATE.has_key(p):
				new_phonemes.append(cls.SIMPLE_TRANSLATE[p])
			else:
				new_phonemes.append(p)
				if not p in [" ", ",", "."]:
					print "there is no '", p, "' in ST"
		i = 0
		while i<len(new_phonemes):
			if new_phonemes[i] == "e" and (i==len(new_phonemes)-1 or not re.match("\w", new_phonemes[i+1])):
				new_phonemes[i] = "ei"
			if new_phonemes[i] == "eo" and (i==len(new_phonemes)-1 or not re.match("\w", new_phonemes[i+1])):
				new_phonemes[i] = "o"
			if new_phonemes[i] == "ci" and (i==len(new_phonemes)-1 or not re.match("\w", new_phonemes[i+1])):
				new_phonemes[i] = "cz"
			if new_phonemes[i] == "zz" and (i==0 or not re.match("\w", new_phonemes[i-1])):
				new_phonemes[i] = "z"
			i += 1
		print "".join(new_phonemes)
		cls.say_festival(new_phonemes)
		return new_phonemes

	@classmethod
	def say_festival(cls, phonemes):
		output = open("synteza_mowy/p1/output.txt", "w")
		output.write('(SayText "'+''.join(phonemes)+'")\n')
		output.close()
		subprocess.call(["festival", "-b", "synteza_mowy/p1/output.txt"])
		os.remove("synteza_mowy/p1/output.txt")
# e$ -> ei$
