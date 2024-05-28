fn timestamp_file() -> String {
    format!("{}", chrono::Utc::now().format("%Y-%m-%d_%H-%M-%SZ"))
}

macro_rules! test {
    ($e:expr) => {
        println!("{} -> {:?}", stringify!($e), $e);
    }
}

fn main() {
    println!("{}", chrono::Utc::now());
    println!("{}", chrono::Local::now());
    println!("{}", chrono::DateTime::parse_from_rfc3339("2020-07-31T23:59:59.000Z").unwrap());
    println!("{}", chrono::DateTime::parse_from_rfc3339("2020-07-31 23:59:59Z").unwrap());
    test!(chrono::NaiveDateTime::parse_from_str("20200101000000hahaha", "%Y%m%d%H%M%S"));
    test!(chrono::DateTime::parse_from_rfc3339("2020-07-31"));
    test!(chrono::DateTime::parse_from_rfc3339("2020-07-31Z"));
    test!(chrono::DateTime::parse_from_rfc2822("2020-07-31"));
    test!(chrono::DateTime::parse_from_rfc2822("2020-07-31Z"));
    test!(chrono::DateTime::from_timestamp(0, 0));
    {
        use chrono::TimeZone;
        test!(
            chrono::Utc.from_utc_datetime(
                &chrono::NaiveDate::parse_from_str("2020-07-31", "%Y-%m-%d")
                    .unwrap()
                    .and_hms_opt(0, 0, 0)
                    .unwrap(),
            )
        );
    }
    println!("{}", timestamp_file());
    println!(
        "{}",
        chrono::DateTime::from_timestamp(253402315200, 0)
            .unwrap()
            .with_timezone(&chrono::FixedOffset::east_opt(-4 * 3600).unwrap()),
    );
}
