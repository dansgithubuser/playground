use std::os::unix::fs::symlink;

fn main() {
    std::fs::remove_file("l").ok();
    symlink("a.txt", "l").unwrap();
    std::fs::remove_file("l").ok();
    symlink("b.txt", "l").unwrap();
}
