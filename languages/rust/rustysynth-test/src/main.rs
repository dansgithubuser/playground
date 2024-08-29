use rustysynth::{
    SoundFont,
    Synthesizer,
    SynthesizerSettings,
};

use std::fs::File;
use std::io::Write;
use std::sync::Arc;

fn main() {
    // Load the SoundFont.
    let mut sf2 = File::open("/home/dan/Desktop/repos/dlal/assets/soundfont/32MbGMStereo.sf2").unwrap();
    let sound_font = Arc::new(SoundFont::new(&mut sf2).unwrap());

    // Create the synthesizer.
    let settings = SynthesizerSettings::new(44100);
    let mut synthesizer = Synthesizer::new(&sound_font, &settings).unwrap();

    // Play some notes (middle C, E, G).
    synthesizer.note_on(0, 60, 100);
    synthesizer.note_on(0, 64, 100);
    synthesizer.note_on(0, 67, 100);

    // The output buffer (3 seconds).
    let sample_count = (3 * settings.sample_rate) as usize;
    let mut left: Vec<f32> = vec![0_f32; sample_count];
    let mut right: Vec<f32> = vec![0_f32; sample_count];

    // Render the waveform.
    synthesizer.render(&mut left[..], &mut right[..]);

    let mut file = File::create("out.f32le").unwrap();
    for i in left {
        file.write(&i.to_le_bytes()).unwrap();
    }
}
