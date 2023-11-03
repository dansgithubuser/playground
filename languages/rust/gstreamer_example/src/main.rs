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
    let cam = gstreamer::ElementFactory::make("v4l2src").build()?;
    let appsink = gstreamer::ElementFactory::make("appsink").build()?;
    pipeline.add(&cam)?;
    pipeline.add(&appsink)?;
    cam.link(&appsink)?;
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
