# -*- coding: utf-8 -*-

from . import MusicSynthesizer
import sys

print "ZAD3: Syntezator muzyczny"


melody_path = "synteza_mowy/p2/melodie/blues.txt"
if len(sys.argv) == 2:
	melody_path = sys.argv[1]

MusicSynthesizer.play(melody_path)
