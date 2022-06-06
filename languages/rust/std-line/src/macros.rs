macro_rules! ctx {
    () => {
        println!("{} {}", file!(), line!());
    };
}

pub(crate) use ctx;
