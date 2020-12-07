fn main() {
    println!("{:?}", std::panic::set_hook(Box::new(|info| {
        println!("panic");
        println!("info: {}", info);
    })));
    panic!("lol");
}
