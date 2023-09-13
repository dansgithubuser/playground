use std::io::Write;
use std::process::{Command, Stdio};

fn main() {
    let child = Command::new("cat")
        .stdin(Stdio::piped())
        .spawn()
        .unwrap();
    child.stdin.as_ref().unwrap().write_all(b"Hello, cat!\n").unwrap();
    child.stdin.as_ref().unwrap().write_all(b"Meow.\n").unwrap();
    drop(child);

    let mut proc = Command::new("python3");
    proc.args(["-c", "import time; time.sleep(5); print('Hello from child!')"]);
    let child = proc.spawn().unwrap();
    drop(child);
    println!("Hello from parent!");
}
