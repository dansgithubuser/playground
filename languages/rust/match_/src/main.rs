use std::thread::sleep;
use std::time::{Duration, Instant};

fn main() {
    let x = Instant::now();
    sleep(Duration::from_secs_f32(0.099));
    let y = Instant::now();
    let d = (y - x).as_millis();
    println!("{}", d);
    match 0 {
        d => println!("Bingo! Kind of."), // this is an assignment, 0 is not being matched to outer d
        _ => println!("Try again."),
    };
}
