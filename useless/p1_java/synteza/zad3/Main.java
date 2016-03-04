package synteza.zad3;

import java.util.ArrayList;

import synteza.zad1.Phonemes;
import synteza.zad2.Syllables;
import synteza.zad3.SimpleSynthesizer;

public class Main {
	public static void main(String[] args) {
		System.out.println("ZAD3: prosty syntezator sklejający fonemy");
		ArrayList<String> phonemes = Syllables.separateSyllables(Phonemes.lineToPhonemes("auto"));
		SimpleSynthesizer.synthesize(phonemes);
	}
}