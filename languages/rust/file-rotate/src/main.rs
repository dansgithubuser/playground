use std::io::Write;

fn print_logs() {
    for path in ["log", "log.1", "log.2"] {
        println!("{}\n{}\n", path, std::fs::read_to_string(path).unwrap_or("-".into()));
    }
}

fn main() {
    let mut log = file_rotate::FileRotate::new(
        "log",
        file_rotate::suffix::AppendCount::new(2),
        file_rotate::ContentLimit::Lines(3),
        file_rotate::compression::Compression::None,
        #[cfg(unix)]
        None,
    );
    for i in 0..10 {
        writeln!(log, "{}", i).ok();
        println!("----- {} -----", i);
        print_logs();
    }
}
