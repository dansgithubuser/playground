struct Double {}

impl Double {
    fn hello() {
        println!("Hello, Bernice.");
    }
}

impl Double {
    fn hello() {
        println!("Hello, Clarence.");
    }
}

fn main() {
    Double::hello();
}
