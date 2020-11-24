fn main() {
    std::thread::spawn(|| {
        panic!("Oh no!");
    });
    std::thread::sleep(std::time::Duration::from_secs(1));
    println!("Main thread finishing gracefully.");
}
