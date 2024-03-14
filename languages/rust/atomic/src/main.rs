use std::sync::atomic;
use std::thread;
use std::time::Duration;

fn main() {
    let b = atomic::AtomicBool::new(false);
    thread::spawn(|| {
        for _ in 0..10 {
            thread::sleep(Duration::from_secs_f32(0.09));
            // doesn't work - this is a useless construct
            // check how to use Arc in ../arc
            b.store(true, atomic::Ordering::Relaxed);
        }
    });
    for _ in 0..10 {
        if b.load(atomic::Ordering::Relaxed) {
            println!("true");
        } else {
            println!("false");
        }
        thread::sleep(Duration::from_secs_f32(0.1));
    }
}
