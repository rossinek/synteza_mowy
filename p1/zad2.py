# -*- coding: utf-8 -*-

from Phonemes import Phonemes
from Syllables import Syllables

print "ZAD2: Podział fonemów na sylaby"
print " ".join(Syllables.separate_syllables(Phonemes.line_to_phonemes(u"Auto nauka wanna zassać RADOSNY zwierzę sarna chłopców")))