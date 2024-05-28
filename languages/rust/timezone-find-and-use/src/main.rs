fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = std::env::args().collect();
    let lat: f64 = match args.get(1) {
        Some(s) => s.parse()?,
        None => 0.0,
    };
    let lon: f64 = match args.get(2) {
        Some(s) => s.parse()?,
        None => 0.0,
    };
    let tz_name: String = tzf_rs::DefaultFinder::new().get_tz_name(lon, lat).into();
    println!("timezone is {}", tz_name);
    let tz: chrono_tz::Tz = tz_name.parse()?;
    let datetime = chrono::DateTime::from_timestamp(946684800, 0)
        .unwrap()
        .with_timezone(&tz);
    println!("{}", datetime);
    Ok(())
}
