package synteza.zad2;

import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.Collections;

import synteza.zad1.Phonemes;

public class Syllables {
	public static ArrayList<String> separateSyllables(ArrayList<String> phonemes) {
		int last_vowel = -1;
		for(int i=0; i<phonemes.size(); i++) {
			if(!Phonemes.isPhoneme(phonemes.get(i))) {
				last_vowel = -1;
			} else if(Phonemes.isVowel(phonemes.get(i))) {
				if(last_vowel >= 0) {
					if(i-last_vowel>2) {
						phonemes.add(last_vowel+2, "|");
					} else {
						phonemes.add(last_vowel+1, "|");						
					}
					i++;
				}
				last_vowel = i;
			}
		}
		return phonemes;
	}
}