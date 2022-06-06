use std::sync::{mpsc, mpsc::Sender};
use std::thread;
use std::time::Duration;

fn main() {
    let mut senders: Vec<Sender<()>> = vec![];
    for i in 0..5 {
        let (tx, rx) = mpsc::channel::<()>();
        senders.push(tx);
        thread::Builder::new()
            .name(format!("TEST THREAD {i}"))
            .spawn(move || {
                rx.recv().unwrap();
            })
            .unwrap();
    }
    thread::sleep(Duration::from_secs_f32(3.0));
    for tx in senders {
        tx.send(()).unwrap();
    }
}
