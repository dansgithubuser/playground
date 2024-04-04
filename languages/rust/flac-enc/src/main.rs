use std::f32::consts::TAU;

fn main() {
    let mut samples = Vec::<i32>::new();
    let mut phase_r = 0.0;
    let mut phase_l = 0.0;
    for i in 0..441_000 {
        let freq_r = 440.0 + 440.0 * (i as f32 / 441_000.0);
        let freq_l = 880.0 - 440.0 * (i as f32 / 441_000.0);
        phase_r += freq_r / 44100.00 * TAU;
        phase_l += freq_l / 44100.00 * TAU;
        if phase_r > TAU { phase_r -= TAU; }
        if phase_l > TAU { phase_l -= TAU; }
        let amp_r = (4000.0 * phase_r.sin()) as i32;
        let amp_l = (4000.0 * phase_l.sin()) as i32;
        samples.push(amp_r);
        samples.push(amp_l);
    }
    println!("encoding");
    let encoder = flacenc::config::Encoder::default();
    let encoder = {
        use flacenc::error::Verify;
        encoder.into_verified().unwrap()
    };
    let flac_stream = flacenc::encode_with_fixed_block_size(
        &encoder,
        flacenc::source::MemSource::from_samples(&samples, 2, 16, 44100),
        2048,
    ).unwrap();
    println!("sinking");
    let mut flac_sink = flacenc::bitsink::ByteSink::new();
    {
        use flacenc::component::BitRepr;
        flac_stream.write(&mut flac_sink).unwrap();
    }
    println!("writing");
    std::fs::write("test.flac", flac_sink.as_slice()).unwrap();
    println!("done");
}
