trait Rofl {
    fn hello() {
        println!("Hello, Walter.");
    }

    fn chitchat() {
        println!("The weather is nice.");
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

    fn chitchat() {
        println!("I have a giant head.");
    }
}

impl Rofl for Lol {
    fn chitchat() {
        println!("I don't believe in shellfish.");
    }
}

fn main() {
    Lol::hello();
    Lol::chitchat();
    Lol::goodbye();
}
