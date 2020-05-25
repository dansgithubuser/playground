use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
enum Rodent {
    Squirrel,
    Rat,
}

#[derive(Debug, Deserialize)]
#[serde(field_identifier, rename_all = "lowercase")]
enum Bird {
    Pigeon,
    Budgie,
    Crow,
    BlueJay,
}

fn main() {
    let squirrel = serde_json::json!(Rodent::Squirrel).to_string();
    println!("{}", squirrel);
    println!("{:?}", serde_json::from_str::<Rodent>(&squirrel));
    println!("{:?}", serde_json::from_str::<Rodent>("\"Squirrel\""));
    println!("{:?}", serde_json::from_str::<Bird>("\"bluejay\""));
}
