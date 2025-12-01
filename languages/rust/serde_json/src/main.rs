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

#[derive(Debug, Deserialize, Serialize)]
struct DoubleOption {
    a: Option<Option<String>>,
}

#[derive(Debug, Deserialize, Serialize)]
struct DoubleOptionSerdeWith {
    #[serde(default, skip_serializing_if = "Option::is_none", with = "serde_with::rust::double_option")]
    a: Option<Option<String>>,
}

#[derive(Debug, Deserialize)]
enum AOrB {
    A,
    B,
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

    // println!("{:?}", json!({ "a": None })); // doesn't compile
    {
        let x: Option<String> = None;
        println!("{:?}", json!({ "a": x }));
    }
    println!("{:?}", json!({ "b": Some(3) }));
    println!("{:?}", json!({ "c": null }));

    {
        let mut j = json!({});
        j["a"] = json!(1);
        println!("{:?}", j);
    }

    println!("{:?}", serde_json::from_str::<DoubleOption>(r#"{}"#));
    println!("{:?}", serde_json::from_str::<DoubleOption>(r#"{"a": null}"#));
    println!("{:?}", serde_json::from_str::<DoubleOption>(r#"{"a": "asdf"}"#));

    println!("{:?}", serde_json::from_str::<DoubleOptionSerdeWith>(r#"{}"#));
    println!("{:?}", serde_json::from_str::<DoubleOptionSerdeWith>(r#"{"a": null}"#));
    println!("{:?}", serde_json::from_str::<DoubleOptionSerdeWith>(r#"{"a": "asdf"}"#));

    // https://github.com/serde-rs/serde/issues/1042

    println!("{:?}", serde_json::from_str::<AOrB>(r#""A""#));
}
