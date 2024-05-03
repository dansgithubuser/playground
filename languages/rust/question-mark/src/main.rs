fn lol() -> Option<()> {
    let x: u32 = Some(3)?;
    if x != 3 { panic!() }
    None?;
    Some(())
}

fn main() {
    lol();
    println!("Hello, world!");
}
