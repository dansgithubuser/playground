use std::thread;
use std::time::Duration;

fn main() {
    thread::spawn(|| {
        thread::sleep(Duration::from_secs(5));
        println!("OK I'm done.");
    });
    println!("Program terminating.");
}
