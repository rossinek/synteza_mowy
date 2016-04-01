# -*- coding: utf-8 -*-

from EnglishSyllables import EnglishSyllables

print "ZAD2: Uczenie się angielskich sylab"


es = EnglishSyllables()
#es.learn("synteza_mowy/p2/cmudict/tl.txt")
#print es.separate_syllables("UW K Y T N Z ER")
es.learn("synteza_mowy/p2/cmudict/learning_set.txt")
(a,t) = es.validate("synteza_mowy/p2/cmudict/validate_set.txt")
print str(a)+'/'+str(t)
print str((float(a)*100.0)/float(t))+' %'
print "from "+str(es.nlearned)+' samples'