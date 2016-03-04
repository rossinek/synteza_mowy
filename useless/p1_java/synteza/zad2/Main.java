package synteza.zad2;

import java.util.ArrayList;

import synteza.zad1.Phonemes;
import synteza.zad2.Syllables;

public class Main {
	public static void main(String [] args) {
		System.out.println("ZAD2: podział fonemów na sylaby");
		ArrayList<String> phonemes = Syllables.separateSyllables(Phonemes.lineToPhonemes("Auto nauka wanna zassać RADOSNY zwierzę sarna chłopców"));
		for (String p : phonemes) {
			System.out.print(p+" ");
		}
		System.out.println();
	}
}