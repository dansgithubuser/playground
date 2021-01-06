fn main() {
    match (1, 2) {
        (_, 2) => println!("a"),
        (1, _) => println!("b"),
        (_, _) => println!("c"),
    }
}
