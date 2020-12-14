fn main() {
    println!("{:?}", std::panic::set_hook(Box::new(|info| {
        println!("panic");
        println!("info: {}", info);
        std::thread::spawn(|| {
            std::thread::sleep(std::time::Duration::from_secs(2));
            std::process::exit(2);
        });
    })));
    panic!("lol");
}
