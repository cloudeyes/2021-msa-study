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

pub type Sku = String;
pub type Integer = f64;

#[derive(Serialize, Deserialize)]
pub struct Batch {
    #[serde(rename = "allocations")]
    allocations: Vec<OrderLine>,

    #[serde(rename = "qty")]
    qty: i64,

    #[serde(rename = "reference")]
    reference: String,

    /// TypeScript-JSON Schema for quicktype code generation.
    #[serde(rename = "sku")]
    sku: String,
}

#[derive(Serialize, Deserialize)]
pub struct OrderLine {
    #[serde(rename = "id")]
    id: String,

    #[serde(rename = "qty")]
    qty: i64,

    /// TypeScript-JSON Schema for quicktype code generation.
    #[serde(rename = "sku")]
    sku: String,
}

#[derive(Serialize, Deserialize)]
pub struct Order {
    #[serde(rename = "orderLines")]
    order_lines: Option<Vec<OrderLine>>,

    #[serde(rename = "reference")]
    reference: String,
}
