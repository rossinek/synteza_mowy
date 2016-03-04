package synteza.zad1;

import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.Collections;

public class Phonemes {
	private static final List<String> Palatalizables;
	static {
		String[] a = {"c","dz","n","s","z"};
		Palatalizables = Arrays.asList(a);
	}
	private static final List<String> Digraphs;
	static {
		String[] a = {"ch","cz","drz","dz","dzi","rz","sz"};
		Digraphs = Arrays.asList(a);
	}
	private static final List<String> Vowels;
	static {
		String[] a = {"a","on","e","en","i","o","u","y"};
		Vowels = Arrays.asList(a);
	}
	private static final Map<String, String> PolishLetters;
	static {
		Map<String, String> map = new HashMap<String, String>();
		map.put("ą", "on");
		map.put("ć", "ci");
		map.put("ę", "en");
		map.put("ł", "ll");
		map.put("ń", "ni");
		map.put("ó", "u");
		map.put("ś", "si");
		map.put("ź", "zi");
		map.put("ż", "rz");
		PolishLetters = Collections.unmodifiableMap(map);
	}
	private static final Map<String, String> VoicelessEquivalents;
	static {
		Map<String, String> map = new HashMap<String, String>();
		map.put("b", "p");
		map.put("d", "t");
		map.put("w", "f");
		map.put("g", "k");
		map.put("z", "s");
		map.put("rz", "sz");
		map.put("drz", "cz");
		map.put("zi", "si");
		map.put("dz", "c");
		map.put("dzi", "ci");
		VoicelessEquivalents = Collections.unmodifiableMap(map);
	}

	private static final Map<String, String> VoicedEquivalents;
	static {
		Map<String, String> map = new HashMap<String, String>();
		for (String key : VoicelessEquivalents.keySet()) {
			map.put(VoicelessEquivalents.get(key), key);
		}
		VoicedEquivalents = Collections.unmodifiableMap(map);
	}

	public static ArrayList<String> lineToPhonemes(String line) {
		line = line.toLowerCase();
		ArrayList<String> phonemes = new ArrayList<String>();
		String[] words = line.split(" ");
		for (String word : words) {
			phonemes.addAll(wordToPhonemes(word));
			phonemes.add(" ");
		}
		return phonemes;
	}

	public static ArrayList<String> wordToPhonemes(String word) {
		word = word.toLowerCase();
		ArrayList<String> phonemes = new ArrayList<String>();
		if(word.length()>0) {
			for(int i=0; i<word.length(); i++) {
				String letter = word.substring(i, i+1);
				String phoneme;
				if((phoneme = PolishLetters.get(letter)) == null) {
					phoneme = letter;
				}

				phonemes.add(phoneme);
			}

			connectDigraphs(phonemes);
			palatalize(phonemes);
			lengthenI(phonemes);
			unnasalizeVowels(phonemes);
			splitNosalVowels(phonemes);
			fixLast(phonemes);
			backwardVoiceless(phonemes);
			forwardVoiceless(phonemes);
			backwardVoiced(phonemes);
			fixLetterU(phonemes);
		}
		return phonemes;
	}

	private static void connectDigraphs(ArrayList<String> phonemes) {
		for(int i=phonemes.size()-1; i>0; i--) {
			if(isDigraph(phonemes.get(i-1), phonemes.get(i))) {
				phonemes.set(i-1, phonemes.get(i-1)+phonemes.get(i));
				phonemes.remove(i);
				i--;
			}
		}
	}

	private static void palatalize(ArrayList<String> phonemes) {
		for(int i=phonemes.size()-1; i>0; i--) {
			if(phonemes.get(i).equals("i") && isPalatalizable(phonemes.get(i-1))) {
				phonemes.set(i-1, phonemes.get(i-1)+"i");
				if(i+1<phonemes.size() && isVowel(phonemes.get(i+1))) {
					phonemes.remove(i);
				}
				i--;
			}
		}
	}

	private static final List<String> prefixesWithAu;
	static {
		String[] a = {"nau","zau","prau","pozau","nienau","niezau","nieprau","niepozau"};
		prefixesWithAu = Arrays.asList(a);
	}

	private static boolean fixAuPrefix(String word) {
		for(String prefix : prefixesWithAu) {
			if(word.startsWith(prefix)) {
				// exceptions:
				//	.*au.o.*
				//	.*au.$
				if(word.length()==prefix.length()+1 || (word.length()>prefix.length()+1 && word.substring(prefix.length()+1, prefix.length()+2).equals("o"))) {
					return false;
				}
				return true;
			}
		}
		return false;
	}

	private static final List<String> prefixesWithEu;
	static {
		String[] a = {"przeu","nieprzeu"};
		prefixesWithEu = Arrays.asList(a);
	}

	private static boolean fixEuPrefix(String word) {
		for(String prefix : prefixesWithEu) {
			if(word.startsWith(prefix)) {
				return true;
			}
		}
		return false;
	}

	// exceptions:
	//	.*eusz.*
	//	.*eusi.*
	//	.*euj.*
	//	.*eu.$
	//	.*aurk.*
	private static final List<String> euExceptionalSuccessors;
	static {
		String[] a = {"sz","si","j"};
		euExceptionalSuccessors = Arrays.asList(a);
	}
	private static void fixLetterU(ArrayList<String> phonemes) {
		String word = concat(phonemes);
		boolean skipFirst = fixAuPrefix(word) || fixEuPrefix(word);
		for(int i=1; i<phonemes.size(); i++) {
			if(phonemes.get(i).equals("u") && (phonemes.get(i-1).equals("a")||phonemes.get(i-1).equals("e"))) {
				if(skipFirst) {
					skipFirst = false;
					continue;
				}
				if(phonemes.get(i-1).equals("e")) {
					if(i+2==phonemes.size()) break;
					if(i+1<phonemes.size() && euExceptionalSuccessors.contains(phonemes.get(i+1))) continue;
				} else {
					if(i+2<phonemes.size() && (phonemes.get(i+1)+phonemes.get(i+2)).equals("rk")) continue;
				}
				phonemes.set(i, "ll");
			}
		}
	}


	private static void lengthenI(ArrayList<String> phonemes) {
		for(int i=0; i<phonemes.size()-1; i++) {
			if(phonemes.get(i).equals("i") && isVowel(phonemes.get(i+1))) {
				phonemes.set(i, "j");
				i++;
			}
		}
	}

	private static void unnasalizeVowels(ArrayList<String> phonemes) {
		for(int i=0; i<phonemes.size()-1; i++) {
			String voiceless;
			if((phonemes.get(i).equals("on") || phonemes.get(i).equals("en")) && (phonemes.get(i+1).equals("l") || phonemes.get(i+1).equals("ll"))) {
				phonemes.set(i, phonemes.get(i).substring(0,1));
				i++;
			}
		}
	}

	// TODO: dz, c (??)
	private static final List<String> nosalVowelsSplitters;
	static {
		String[] a = {"t","d","b","p","ci","dzi","dz","c"};
		nosalVowelsSplitters = Arrays.asList(a);
	}
	private static void splitNosalVowels(ArrayList<String> phonemes) {
		for(int i=0; i<phonemes.size()-1; i++) {
			String voiceless;
			if((phonemes.get(i).equals("on") || phonemes.get(i).equals("en")) && nosalVowelsSplitters.contains(phonemes.get(i+1))) {
				if(phonemes.get(i+1).equals("b")) {
					phonemes.add(i+1, "m");
				} else {
					phonemes.add(i+1, phonemes.get(i).substring(1,2));					
				}
				phonemes.set(i, phonemes.get(i).substring(0,1));
				i+=2;
			}
		}
	}

	private static void fixLast(ArrayList<String> phonemes) {
		String voiceless;
		if(phonemes.size()>1) {
			if((voiceless=VoicelessEquivalents.get(phonemes.get(phonemes.size()-1)))!=null) {
				phonemes.set(phonemes.size()-1, voiceless);
			}
			if(phonemes.get(phonemes.size()-1).equals("en")) {
				phonemes.set(phonemes.size()-1, "e");
			}
		}
	}

	private static void backwardVoiceless(ArrayList<String> phonemes) {
		for(int i=0; i<phonemes.size()-1; i++) {
			String voiceless;
			if((voiceless=VoicelessEquivalents.get(phonemes.get(i)))!=null && VoicedEquivalents.get(phonemes.get(i+1))!=null) {
				phonemes.set(i, voiceless);
				i++;
			}
		}
	}

	private static void forwardVoiceless(ArrayList<String> phonemes) {
		for(int i=phonemes.size()-1; i>0; i--) {
			String voiceless;
			if(VoicedEquivalents.get(phonemes.get(i-1))!=null && (voiceless=VoicelessEquivalents.get(phonemes.get(i)))!=null && (voiceless.equals("f")||voiceless.equals("sz"))) {
				phonemes.set(i, voiceless);
				i--;
			}
		}
	}

	private static void backwardVoiced(ArrayList<String> phonemes) {
		for(int i=0; i<phonemes.size()-1; i++) {
			String voiceless;
			if((voiceless=VoicedEquivalents.get(phonemes.get(i)))!=null && VoicelessEquivalents.get(phonemes.get(i+1))!=null) {
				phonemes.set(i, voiceless);
				i++;
			}
		}
	}

	public static boolean isDigraph(String l1, String l2) {
		String d=l1+l2;
		return Digraphs.contains(d);
	}

	public static boolean isPalatalizable(String l) {
		return Palatalizables.contains(l);
	}

	public static boolean isVowel(String l) {
		return Vowels.contains(l);
	}

	public static boolean isConsonant(String l) {
		return !isVowel(l);
	}

	private static String concat(ArrayList<String> al) {
		String str = "";
		for(String s : al) {
			str+=s;
		}
		return str;
	}

	public static boolean isPhoneme(String l) {
		return Pattern.compile("[a-z]{1,3}").matcher(l).find();
	}
}