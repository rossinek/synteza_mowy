# -*- coding: utf-8 -*-

from ..p1.Phonemes import Phonemes

print "ZAD1: Testowanie zadania 1 z pracowni 1"

debug = raw_input("Debug mode? [y/N]: ")
if debug in ["y", "Y"]:
	debug = True
else: 
	debug = False

tests_file = open("synteza_mowy/p2/testy_wyglos.txt", "r")
naccepted = 0
ntotal = 0
for line in tests_file.readlines():
	line = line.split("#")[0].lower()
	temp = line.split()
	if len(temp) != 2:
		continue
	[q, a] = temp
	my_a = "-".join(Phonemes.line_to_phonemes(q.decode("utf-8")))
	if(my_a == a):
		naccepted += 1
		if debug:
			print " ✓ ", q, ": ", my_a
	else:
		print " ✗ ", q
		print "      ▸ ", a, " ◂ "
		print "        ", my_a
	ntotal += 1

print "accepted: ", naccepted, "/", ntotal

tests_file.close()