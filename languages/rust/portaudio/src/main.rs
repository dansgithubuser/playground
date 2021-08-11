use portaudio as pa;

fn main() -> Result<(), pa::Error> {
    const SAMPLE_RATE: f64 = 8000.0;
    const RUN_SIZE: u32 = 1024;
    const CHANNELS: i32 = 2;
    const INTERLEAVED: bool = true;
    let pa = pa::PortAudio::new()?;
    let devices = pa.devices()?;
    for device in devices {
        println!("{:?}", device);
    }
    let input_device = pa.default_input_device()?;
    let input_params = pa::StreamParameters::<f32>::new(
        input_device,
        CHANNELS,
        INTERLEAVED,
        pa.device_info(input_device)?.default_high_input_latency,
    );
    let output_device = pa.default_output_device()?;
    let output_params = pa::StreamParameters::<f32>::new(
        output_device,
        CHANNELS,
        INTERLEAVED,
        pa.device_info(output_device)?.default_high_output_latency,
    );
    pa.is_duplex_format_supported(input_params, output_params, SAMPLE_RATE)?;
    let mut stream = pa.open_non_blocking_stream(
        pa::DuplexStreamSettings::new(
            input_params,
            output_params,
            SAMPLE_RATE,
            RUN_SIZE,
        ),
        move |args| {
            for (i, output_sample) in args.out_buffer.iter_mut().enumerate() {
                *output_sample = i as f32 / RUN_SIZE as f32;
            }
            println!("{}", args.in_buffer.iter().sum::<f32>());
            pa::Continue
        },
    )?;
    stream.start()?;
    std::thread::sleep(std::time::Duration::from_secs(4));
    Ok(())
}
