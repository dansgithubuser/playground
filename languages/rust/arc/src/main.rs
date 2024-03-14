use std::sync::Arc;
use std::thread;
use std::time::Duration;

fn main() {
    let arc = Arc::new(());
    for i in 0..10 {
        let clone = arc.clone();
        thread::spawn(move || {
            thread::sleep(Duration::from_secs_f32(i as f32 / 20.0));
            drop(clone);
        });
    }
    for _ in 0..10 {
        println!("strong count: {}, weak count: {}", Arc::strong_count(&arc), Arc::weak_count(&arc));
        thread::sleep(Duration::from_secs_f32(0.1));
    }
}
