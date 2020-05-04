fn sub(text: String) {
    println!("text: {}", text);
    println!(
        "sub: {}",
        regex::Regex::new(concat!(
            r"%(?P<component>\d+)",
            r"(?:\*(?P<m>[\d.e-]+))?",
            r"(?:\+(?P<b>[\d.e-]+))?",
        ))
            .unwrap()
            .replace_all(
                &text,
                |captures: &regex::Captures| -> String {
                    println!("captures: {:?}", captures);
                    let i = captures.get(1).unwrap().as_str().parse::<i32>().unwrap();
                    let m = captures.get(2).map_or(1, |v| v.as_str().parse::<i32>().unwrap());
                    let b = captures.get(3).map_or(0, |v| v.as_str().parse::<i32>().unwrap());
                    (i * m + b).to_string()
                },
            ),
    )
}

fn main() {
    sub(r#"{
        "name": "hello",
        "args": [
            %0,
            %1*4,
            %1+5,
            %2*3+2,
        ]
    }"#.into());
}
