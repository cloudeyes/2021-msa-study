#[derive(Default)]
pub struct Batch {
    reference: String,
    sku: String,
    qty: i64,
    allocations: Vec<OrderLine>,
}

pub struct OrderLine {
    id: String,
    sku: String,
    qty: i64,
}

#[derive(Default)]
pub struct Order {
    reference: String,
    order_lines: Vec<OrderLine>,
}

impl PartialEq for Batch {
    fn eq(&self, other: &Self) -> bool {
        return &self.reference == &other.reference;
    }
}

fn add(a: i64, b: i64) -> i64 {
    return a + b;
}

fn bad_add(a: i64, _b: i64) -> i64 {
    return a + 1;
}

#[cfg(test)]
mod tests {
    use super::*; // importing names from outer (for mod tests) scope.

    #[test]
    fn test_add() {
        assert_eq!(add(1, 2), 3);
    }

    #[test]
    fn test_bad_add() {
        assert_eq!(bad_add(1, 2), 3);
    }
}

fn main() {
    println!("Hello, world!");
}
