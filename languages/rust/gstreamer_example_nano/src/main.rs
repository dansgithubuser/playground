/*
- https://gstreamer.freedesktop.org/documentation/application-development/index.html?gi-language=c
- https://gstreamer.pages.freedesktop.org/gstreamer-rs/stable/latest/docs/gstreamer/index.html#
- https://github.com/sdroege/gstreamer-rs/blob/main/examples/src/bin/appsink.rs
*/

use gstreamer::prelude::{
    ElementExt,
    ElementExtManual,
    GstBinExt,
    GstObjectExt,
};

use std::str::FromStr;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    gstreamer::init()?;
    println!("GStreamer version: {:?}", gstreamer::version());
    let pipeline = gstreamer::Pipeline::new();
    let cam = gstreamer::ElementFactory::make("nvarguscamerasrc").build()?;
    let nvvidconv = gstreamer::ElementFactory::make("nvvidconv").build()?;
    let videoconvert1 = gstreamer::ElementFactory::make("videoconvert").build()?;
    let videoconvert2 = gstreamer::ElementFactory::make("videoconvert").build()?;
    let appsink = gstreamer_app::AppSink::builder().build();
    pipeline.add(&cam)?;
    pipeline.add(&nvvidconv)?;
    pipeline.add(&videoconvert1)?;
    pipeline.add(&videoconvert2)?;
    pipeline.add(&appsink)?;
    cam.link_filtered(
        &nvvidconv,
        &gstreamer::caps::Caps::from_str("video/x-raw(memory:NVMM),width=1440,height=1080,framerate=15/1")?,
    )?;
    nvvidconv.link_filtered(
        &videoconvert1,
        &gstreamer::caps::Caps::from_str("video/x-raw,width=1440,height=1080,framerate=15/1")?,
    )?;
    videoconvert1.link_filtered(
        &videoconvert2,
        &gstreamer::caps::Caps::from_str("video/x-raw,format=BGRx")?,
    )?;
    videoconvert2.link_filtered(
        &appsink,
        &gstreamer::caps::Caps::from_str("video/x-raw,format=BGR")?,
    )?;
    appsink.set_callbacks(
        gstreamer_app::AppSinkCallbacks::builder()
            .new_sample(|appsink| {
                let sample = appsink.pull_sample().map_err(|_| gstreamer::FlowError::Eos)?;
                let buffer = sample.buffer().ok_or_else(|| {
                    gstreamer::element_error!(
                        appsink,
                        gstreamer::ResourceError::Failed,
                        ("Failed to get buffer from appsink")
                    );
                    gstreamer::FlowError::Error
                })?;
                let map = buffer.map_readable().map_err(|_| {
                    gstreamer::element_error!(
                        appsink,
                        gstreamer::ResourceError::Failed,
                        ("Failed to map buffer readable")
                    );
                    gstreamer::FlowError::Error
                })?;
                let slice = map.as_slice();
                println!(
                    "rough avg: {:.1}, len: {}",
                    slice.iter().step_by(100).map(|i| *i as f32).sum::<f32>() * 100.0 / slice.len() as f32,
                    slice.len(),
                );
                Ok(gstreamer::FlowSuccess::Ok)
            })
            .build(),
    );
    pipeline.set_state(gstreamer::State::Playing)?;
    let bus = pipeline.bus().unwrap(); // pipeline without bus shouldn't happen
    for msg in bus.iter_timed(gstreamer::ClockTime::NONE) { // don't timeout
        match msg.view() {
            gstreamer::MessageView::Eos(..) => break,
            gstreamer::MessageView::Error(err) => {
                eprintln!(
                    "Received error from {}: {} (debug: {:?})",
                    msg
                        .src()
                        .map(|src| src.path_string().to_string())
                        .unwrap_or("UNKNOWN".into()),
                    err.error(),
                    err.debug(),
                );
                break;
            }
            _ => (),
        }
    }
    pipeline.set_state(gstreamer::State::Null)?;
    Ok(())
}
