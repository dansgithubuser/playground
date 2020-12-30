macro_rules! format_test {
    ($fmt:expr) => {
        print!("{} ", $fmt);
        let x = [
            1.0,
            10.0,
            0.1,
            1234567890.0,
            -0.123456789,
            1.23456789e40,
            -1.23456789e-40,
        ];
        for i in &x {
            print!($fmt, i);
            print!(" ");
        }
        println!("");
    }
}

fn main() {
    format_test!("{}");
    format_test!("{:}");
    format_test!("{:.}");
    format_test!("{:.2}");
    format_test!("{:.6}");
    format_test!("{:>10.6}");
    format_test!("{:0>10.6}");
    format_test!("{:e}");
    format_test!("{:.2e}");
    format_test!("{:.6e}");
}
