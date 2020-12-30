trait Rofl {
    fn hello() {
        println!("Hello, Walter.");
    }

    fn goodbye() {
        println!("Goodbye, Walter.");
    }
}

struct Lol {}

impl Lol {
    fn hello() {
        println!("Hello, George.");
    }
}

impl Rofl for Lol {}

fn main() {
    Lol::hello();
    Lol::goodbye();
}
