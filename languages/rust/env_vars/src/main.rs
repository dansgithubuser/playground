fn main() {
    std::env::set_var("lol", "rofl");
    println!("{:?}", std::env::var("lol"));
    std::env::set_var("lol", "lmao");
    println!("{:?}", std::env::var("lol"));
}
