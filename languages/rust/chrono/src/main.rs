fn timestamp_file() -> String {
    format!("{}", chrono::Utc::now().format("%Y-%m-%d_%H-%M-%SZ"))
}

fn main() {
    println!("{}", chrono::Utc::now());
    println!("{}", chrono::Local::now());
    println!("{}", chrono::DateTime::parse_from_rfc3339("2020-07-31T23:59:59.000Z").unwrap());
    println!("{:?}", chrono::NaiveDateTime::parse_from_str("20200101000000hahaha", "%Y%m%d%H%M%S"));
    println!("{:?}", chrono::DateTime::parse_from_rfc3339("2020-07-31"));
    println!("{:?}", chrono::DateTime::parse_from_rfc3339("2020-07-31Z"));
    println!("{:?}", chrono::DateTime::parse_from_rfc2822("2020-07-31"));
    println!("{:?}", chrono::DateTime::parse_from_rfc2822("2020-07-31Z"));
    {
        use chrono::TimeZone;
        println!(
            "{}",
            chrono::Utc.from_utc_datetime(
                &chrono::NaiveDate::parse_from_str("2020-07-31", "%Y-%m-%d")
                    .unwrap()
                    .and_hms_opt(0, 0, 0)
                    .unwrap(),
            ),
        );
    }
    println!("{}", timestamp_file());
}
