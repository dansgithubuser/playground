macro_rules! check {
    ($e:expr) => {
        println!("{} --> {}", stringify!($e), $e);
    }
}

fn main() {
    check!(0.0 % 360.0);
    check!(180.0 % 360.0);
    check!(360.0 % 360.0);
    check!(540.0 % 360.0);
    check!(-90.0 % 360.0);
    check!((-90.0f32).rem_euclid(360.0));
}
