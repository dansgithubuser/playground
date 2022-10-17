fn main() {
        let mut co = fs_extra::dir::CopyOptions::default();
        co.overwrite = true;
        co.copy_inside = true;
        let r = fs_extra::dir::copy("src", "copy/src", &co);
        println!("{:?}", r);
}
