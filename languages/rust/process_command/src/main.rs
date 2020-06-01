fn main() {
    println!(
        "{:?}",
        std::process::Command::new("journalctl")
            .args(&["-S", "2020-01-01UTC"])
            .output(),
    );
}
