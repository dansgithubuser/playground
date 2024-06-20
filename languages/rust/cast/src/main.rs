macro_rules! test {
    ($e:expr) => {
        println!("{} is {}", stringify!($e), $e);
    };
}

fn main() {
    test!(-1i64 as u64);
    test!(123456.0f32 as i16);
    test!(-123456.0f32 as i16);
}
