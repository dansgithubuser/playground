use std::sync::mpsc::channel;
use std::thread;
use std::time::Duration;

fn main() {
    let (sender, receiver) = channel();
    thread::spawn(move|| {
        sender.send("lol").unwrap();
        thread::sleep(Duration::from_millis(5000));
    });
    println!("{:?}", receiver.recv().unwrap());
    println!("{:?}", receiver.recv_timeout(Duration::from_millis(1000)).unwrap());
}
