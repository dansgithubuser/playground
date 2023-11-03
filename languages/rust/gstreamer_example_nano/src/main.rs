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

fn main() -> Result<(), Box<dyn std::error::Error>> {
    gstreamer::init()?;
    println!("GStreamer version: {:?}", gstreamer::version());
    let pipeline = gstreamer::Pipeline::new();
    let cam = gstreamer::ElementFactory::make("nvarguscamerasrc").build()?;
    let nvvidconv = gstreamer::ElementFactory::make("nvvidconv").build()?;
    let videoconvert = gstreamer::ElementFactory::make("videoconvert").build()?;
    let appsink = gstreamer_app::AppSink::builder().build();
    pipeline.add(&cam)?;
    pipeline.add(&nvvidconv)?;
    pipeline.add(&videoconvert)?;
    pipeline.add(&appsink)?;
    cam.link_filtered(
        &nvvidconv,
        &gstreamer::caps::Caps::builder_full()
            .structure_with_features(
                gstreamer::structure::Structure::builder("video/x-raw")
                    .field("width", 1440)
                    .field("height", 1080)
                    .field("framerate", gstreamer::Fraction::new(15, 1))
                    .build(),
                {
                    let mut caps_features = gstreamer::CapsFeatures::new_empty();
                    caps_features.add("memory:NVMM");
                    caps_features
                },
            )
            .build(),
    )?;
    nvvidconv.link_filtered(
        &videoconvert,
        &gstreamer::caps::Caps::builder("video/x-raw")
            .field("width", 1440)
            .field("height", 1080)
            .field("framerate", gstreamer::Fraction::new(15, 1))
            .build(),
    )?;
    videoconvert.link_filtered(
        &appsink,
        &gstreamer::caps::Caps::builder("video/x-raw")
            .field("format", "I420") // BGR is very slow!
            .build(),
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
                    "avg: {:.1}, len: {}",
                    slice.iter().map(|i| *i as f32).sum::<f32>() / slice.len() as f32,
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
