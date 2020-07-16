use serde::{ Deserialize, Serialize };
use serde_json::json;

use std::vec::Vec;

#[derive(Debug, Deserialize, Serialize)]
struct Element {
    a: Option<String>,
}

#[derive(Debug, Deserialize, Serialize)]
struct Array {
    arr: Vec<Element>,
}

fn main() {
    println!("{}", json!(Array { arr: vec![Element { a: None }] }).to_string());
    println!("{:?}", serde_json::from_str::<Array>(r#"{"arr": [{}]}"#));

    println!("");

    let val = json!({
        "a": 1,
        "b": 2,
    });
    let obj = val.as_object().unwrap();

    obj.iter().map(|i| println!("{}: {}", i.0, i.1)).for_each(drop);

    println!("");

    for i in obj {
        println!("{}: {}", i.0, i.1);
    }
}
