fn main() {
    let mut proc = std::process::Command::new("python3");
    proc.args(["-c", "import time; time.sleep(5); print('Hello from child!')"]);
    let child = proc.spawn().unwrap();
    drop(child);
    println!("Hello from parent!");
}
