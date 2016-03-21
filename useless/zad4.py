# -*- coding: utf-8 -*-

import re

from enPhonemes import EnPhonemes
from Phonemes import Phonemes

print "ZAD4: Czytanie za pomocą programu festval"

line = ""
line = raw_input("Wpisz tekst (exit): ")
while not re.match("q|exit|quit|$", line):
	ps = Phonemes.line_to_phonemes(line.decode("utf-8"))
	EnPhonemes.simple_translator(ps)
	line = raw_input("Wpisz tekst (exit): ")

