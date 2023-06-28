fn main() {
    let path = std::ffi::CString::new(".").unwrap();
    let (code, stat) = unsafe {
        let mut stat: libc::statvfs = std::mem::zeroed();
        (libc::statvfs(path.as_ptr(), &mut stat), stat)
    };
    println!("code: {}", code);
    println!("file system size in MB: {}", stat.f_blocks * stat.f_frsize / 1_000_000);
    println!("available space in MB: {}", stat.f_bavail * stat.f_frsize / 1_000_000);
}
