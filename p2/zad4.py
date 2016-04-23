# -*- coding: utf-8 -*-

from WaveAnalyzer import WaveAnalyzer

print "ZAD4: Dzielenie w miejscach ciszy"

wa = WaveAnalyzer("synteza_mowy/p2/sylaby/sylaby1.wav")
w = wa.split(51)
w.save("synteza_mowy/p2/output.wav")