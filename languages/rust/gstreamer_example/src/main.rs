/*
- https://gstreamer.freedesktop.org/documentation/application-development/index.html?gi-language=c
- https://gstreamer.pages.freedesktop.org/gstreamer-rs/stable/latest/docs/gstreamer/index.html#
- https://github.com/sdroege/gstreamer-rs/blob/main/examples/src/bin/appsink.rs
*/

use gstreamer::prelude::{ElementExtManual, GstBinExt};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    gstreamer::init()?;
    println!("GStreamer version: {:?}", gstreamer::version());
    let pipeline = gstreamer::Pipeline::new();
    let cam = gstreamer::ElementFactory::make("v4l2src").build()?;
    let appsink = gstreamer::ElementFactory::make("appsink").build()?;
    pipeline.add(&cam)?;
    pipeline.add(&appsink)?;
    cam.link(&appsink)?;
    Ok(())
}
