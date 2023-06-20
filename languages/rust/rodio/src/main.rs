use rodio::Source;

use std::time::Duration;

pub struct SqrWave {
    freq: f32,
    num_sample: usize,
}

impl SqrWave {
    #[inline]
    pub fn new(freq: f32) -> SqrWave {
        SqrWave {
            freq: freq,
            num_sample: 0,
        }
    }
}

impl Iterator for SqrWave {
    type Item = f32;

    #[inline]
    fn next(&mut self) -> Option<f32> {
        self.num_sample = self.num_sample.wrapping_add(1);

        Some(
            if (self.freq * self.num_sample as f32 / 48000.0).fract() < 0.5 {
                1.0
            } else {
                -1.0
            }
        )
    }
}

impl Source for SqrWave {
    #[inline]
    fn current_frame_len(&self) -> Option<usize> {
        None
    }

    #[inline]
    fn channels(&self) -> u16 {
        1
    }

    #[inline]
    fn sample_rate(&self) -> u32 {
        48000
    }

    #[inline]
    fn total_duration(&self) -> Option<Duration> {
        None
    }
}

fn main() -> Result<(), String> {
    let (_out_stream, out_stream_handle) = rodio::OutputStream::try_default().map_err(|e| format!("{}", e))?;
    out_stream_handle.play_raw(
        SqrWave::new(440.0)
            .take_duration(Duration::from_secs_f32(1.0))
            .amplify(0.20),
    ).map_err(|e| format!("{}", e))?;
    std::thread::sleep(Duration::from_secs_f32(1.5));
    Ok(())
}
