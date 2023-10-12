use std::fs;
use std::path::Path;

fn main() {
    let metadata = fs::metadata(Path::new("Cargo.toml")).unwrap();
    println!("{:?}", metadata);
}
