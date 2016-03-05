# -*- coding: utf-8 -*-

import sys
import subprocess
import re

from Phonemes import Phonemes
from Syllables import Syllables
from SimpleSynthesizer import SimpleSynthesizer

print "ZAD3: Prosty syntezator"

line = ""
line = raw_input("Wpisz tekst (exit): ")
while not re.match("q|exit|quit|$", line):
	try:
		phonemes_set = input("Zbiór fonemów (0): ")
	except:
		phonemes_set = 0
	phonemes = Syllables.separate_syllables(Phonemes.line_to_phonemes(line.decode("utf-8")))
	print "> ", " ".join(phonemes)
	SimpleSynthesizer.synthesize(phonemes, phonemes_set)
	line = raw_input("Wpisz tekst (exit): ")