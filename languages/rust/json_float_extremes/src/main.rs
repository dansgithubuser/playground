use serde_json::{json, Value};

fn main() {
    println!("{:?}", json!(f64::MIN));
    println!("{:?}", json!(f64::MAX));
    println!("{:?}", json!(f64::MIN).to_string());
    println!("{:?}", json!(f64::MAX).to_string());
    println!("{:?}", serde_json::from_str::<Value>(&json!(f64::MIN).to_string()));
    println!("{:?}", serde_json::from_str::<Value>(&json!(f64::MAX).to_string()));
    println!("{:?}", serde_json::from_str::<Value>(&json!(f64::MIN).to_string()).unwrap().as_f64().unwrap());
    println!("{:?}", serde_json::from_str::<Value>(&json!(f64::MAX).to_string()).unwrap().as_f64().unwrap());
    println!("{:?}", serde_json::from_str::<Value>("1e1000"));
    {
        let mut s = "17976931348623157".to_string();
        s.push_str(&"0".repeat(308));
        println!("{:?}", serde_json::from_str::<Value>(&s));
    }
}
