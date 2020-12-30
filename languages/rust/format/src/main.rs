macro_rules! format_test {
    ($fmt:expr) => {
        print!("{} ", $fmt);
        let x = [
            [1, 2, 3, 100, 2000],
        ];
        for i in &x {
            print!($fmt, i);
            print!(" ");
        }
        println!("");
    }
}

fn main() {
    format_test!("{:?}");
    format_test!("{:x?}");
    format_test!("{:2x?}");
    format_test!("{:02x?}");
    format_test!("{:>2x?}");
    format_test!("{:0>2x?}");
}
