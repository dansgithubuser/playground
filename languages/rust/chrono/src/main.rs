fn main() {
    println!("{}", chrono::Utc::now());
    println!("{}", chrono::Local::now());
    println!("{}", chrono::DateTime::parse_from_rfc3339("2020-07-31T23:59:59.000Z").unwrap());
}
