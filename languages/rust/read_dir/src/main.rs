fn main() {
    for entry in std::fs::read_dir(".").unwrap() {
        let entry = entry.unwrap();
        println!("{}", entry.path().display());
    }
}
