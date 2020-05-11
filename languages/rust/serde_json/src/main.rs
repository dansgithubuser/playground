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
}
