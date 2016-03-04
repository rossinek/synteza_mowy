package synteza.zad1;

import java.util.ArrayList;

import synteza.zad1.Phonemes;

public class Main {
	public static void main(String [] args) {
		System.out.println("ZAD1: Zamiana na fonemy");
		ArrayList<String> phonemes = Phonemes.lineToPhonemes("będę będą wziął wzięty zięć piędź więc sini");
		for (String p : phonemes) {
			System.out.print(p+" ");
		}
		System.out.println();
	}
}