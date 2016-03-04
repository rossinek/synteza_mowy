package synteza.zad3;

import java.util.ArrayList;
import java.util.Collections;
import java.io.File;
import java.io.IOException;
import java.io.SequenceInputStream;
import javax.sound.sampled.*;

import synteza.zad1.Phonemes;

public class SimpleSynthesizer {

	private static final String WAV_PATH = "synteza/zad3/fonemy/";

	/*public static void synthesize(ArrayList<String> phonemes) {
		ArrayList<AudioInputStream> wavList = new ArrayList<AudioInputStream>();
		
		try {
			long frameLengthSum = 0;
			for (String p : phonemes) {
				if(Phonemes.isPhoneme(p)) {
					AudioInputStream pWav = AudioSystem.getAudioInputStream(new File(WAV_PATH+p+".wav"));
					wavList.add(pWav);
					frameLengthSum+=pWav.getFrameLength();
				}
			}
			SequenceInputStream sis = new SequenceInputStream(Collections.enumeration(wavList));
			AudioInputStream appendedFiles = 
				new AudioInputStream(
					sis,
					wavList.get(0).getFormat(),
					frameLengthSum);

			AudioSystem.write(
				appendedFiles,
				AudioFileFormat.Type.WAVE,
				new File("wavAppended.wav"));

		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	*/

	public static void synthesize(ArrayList<String> phonemes) {

	try {
		File fileOut = new File("appended.wav");
AudioFileFormat.Type fileType = fileFormat.getType();
if (AudioSystem.isFileTypeSupported(fileType, 
    audioInputStream)) {
  AudioSystem.write(audioInputStream, fileType, fileOut);
}


}