// Example code that deserializes and serializes the model.
// extern crate serde;
// #[macro_use]
// extern crate serde_derive;
// extern crate serde_json;
//
// use generated_module::[object Object];
//
// fn main() {
//     let json = r#"{"answer": 42}"#;
//     let model: [object Object] = serde_json::from_str(&json).unwrap();
// }

extern crate serde_derive;

pub type Integer = f64;

#[derive(Serialize, Deserialize)]
pub struct Batch {
    reference: String,
    sku: String,
    qty: i64,
    allocations: Vec<OrderLine>,
}

#[derive(Serialize, Deserialize)]
pub struct OrderLine {
    id: String,
    sku: String,
    qty: i64,
}

#[derive(Serialize, Deserialize)]
pub struct Order {
    reference: String,
    #[serde(rename = "orderLines")]
    order_lines: Vec<OrderLine>,
}
