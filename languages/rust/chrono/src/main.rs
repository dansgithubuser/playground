fn timestamp_file() -> String {
    format!("{}", chrono::Utc::now().format("%Y-%m-%d_%H-%M-%SZ"))
}

fn main() {
    println!("{}", chrono::Utc::now());
    println!("{}", chrono::Local::now());
    println!("{}", chrono::DateTime::parse_from_rfc3339("2020-07-31T23:59:59.000Z").unwrap());
    println!("{:?}", chrono::NaiveDateTime::parse_from_str("20200101000000hahaha", "%Y%m%d%H%M%S"));
    println!("{}", timestamp_file());
}
