use std::io::{prelude::*, stdin};

fn main() {
    println!("Enter to continue, ctrl-c to exit.");
    stdin().read(&mut [0u8]).ok();
    println!("Done.");
}
