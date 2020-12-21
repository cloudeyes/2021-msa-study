use std::cell::RefCell;
use std::cmp::Ordering;
use chrono::{Date, Utc, Duration};

#[derive(PartialEq, Eq, Clone)]
pub struct OrderLine {
    pub reference: String,
    pub sku: String,
    pub qty: i64,
}

#[derive(Default)]
pub struct Batch {
    pub reference: String,
    pub sku: String,
    pub qty: i64,
    pub eta: Option<Date<Utc>>,
    allocations: RefCell<Vec<OrderLine>>
}

// For entity's identity equality
impl PartialEq for Batch {
    fn eq(&self, other: &Self) -> bool {
        &self.reference == &other.reference
    }
}

impl Eq for Batch {}

// For custom ordering
impl PartialOrd for Batch {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Batch {
    fn cmp(&self, other: &Self) -> Ordering {
        let x = (self.eta, other.eta);
        match x {
            (None, _) => Ordering::Less,
            (_, None) => Ordering::Greater,
            (Some(a), Some(b)) => a.cmp(&b)
        }
    }    
}

impl Batch {    
    fn allocate(&self, line: OrderLine){  
        self.allocations.borrow_mut().push(line)
    }

    fn allocated_quantity(&self) -> i64 {
        self.allocations.borrow().iter().fold(0, |sum, it| sum + it.qty)
    }

    fn available_quantity(&self) -> i64 {
        &self.qty - &self.allocated_quantity()
    }
    
    fn can_allocate(&self, line: &OrderLine) -> bool {
        &self.sku == &line.sku && &self.available_quantity() >= &line.qty
    }
}

use std::fmt;

#[derive(Debug, Clone, PartialEq)]
struct OutOfStock;

impl fmt::Display for OutOfStock {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Out of stock!")
    }
}

fn allocate(line: OrderLine, mut batches: Vec<&Batch>) -> Result<String, OutOfStock> {
    batches.sort();
    let filtered = batches.iter().filter(|it| it.can_allocate(&line)).collect::<Vec<&&Batch>>();
    match filtered.first() {
        None => Err(OutOfStock),
        Some(b) => {
            b.allocate(line);
            Ok(b.reference.to_owned())
        }
    }
}

fn make_batch(reference: &str, sku: &str, qty: i64, eta: Option<Date<Utc>>) -> Batch {
    return Batch { 
        reference: reference.to_owned(), sku: sku.to_owned(), qty: qty, eta: eta,
        ..Default::default()
    };
}

fn make_line(reference: &str, sku: &str, qty: i64) -> OrderLine {
    return OrderLine { 
        reference: reference.to_owned(), sku: sku.to_owned(), qty: qty,
    };
}

fn make_batch_and_line(sku: &str, batch_qty: i64, line_qty: i64) -> (Batch, OrderLine) {
    return (
        make_batch("batch-001", sku, batch_qty, Some(Utc::today())),
        make_line("order-123", sku, line_qty)
    )
}

#[cfg(test)]
mod chapter1_tests {
    use super::*; // importing names from outer scope.
    
    #[test]
    fn test_allocating_to_a_batch_reduces_the_available_quantity() {
        let today: Date<Utc>    = Utc::today();
        let batch = make_batch("batch-001", "SMALL-TABLE", 20, Some(today));
        let line = make_line("order-ref", "SMALL-TABLE", 2);

        batch.allocate(line);
        
        assert_eq!(18, batch.available_quantity());
    }

    #[test]
    fn test_can_allocate_if_available_greater_than_required() {
        let (large_batch, small_line) = make_batch_and_line("ELEGANT-LAMP", 20, 2);
        assert!(large_batch.can_allocate(&small_line));
    }

    #[test]
    fn test_cannot_allocate_if_available_smaller_than_required() {
        let (small_batch, large_line) = make_batch_and_line("ELEGANT-LAMP", 2, 20);
        assert!(small_batch.can_allocate(&large_line) == false)
    }

    #[test]
    fn test_can_allocate_if_available_equal_to_required() {
        let (batch, line) = make_batch_and_line("ELEGANT-LAMP", 2, 2);
        assert!(batch.can_allocate(&line));
    }

    #[test]
    fn test_prefers_warehouse_batches_to_shipments() {
        let tomorrow = Utc::today() + Duration::days(1);
        let warehouse_batch = make_batch("warehouse-batch", "RETRO-CLOCK", 100, None);
        let shipment_batch  = make_batch("shipment-batch", "RETRO-CLOCK", 100, Some(tomorrow));
        let line = make_line("oref", "RETRO-CLOCK", 10);

        let batch_ref = allocate(line, vec![&warehouse_batch, &shipment_batch]);
        assert_eq!(Ok("warehouse-batch".to_owned()), batch_ref);
    }

    #[test]
    fn test_prefers_earlier_batches() {
        let today = Utc::today();
        let tomorrow: Date<Utc> = today + Duration::days(1);
        let later: Date<Utc>    = today + Duration::days(30);

        let earliest = make_batch("speedy-batch", "MINIMALIST-SPOON", 100, Some(today));
        let medium   = make_batch("normal-batch", "MINIMALIST-SPOON", 100, Some(tomorrow));
        let latest   = make_batch("slow-batch", "MINIMALIST-SPOON", 100, Some(later));
        let line     = make_line("order-001", "MINIMALIST-SPOON", 10);

        let batch_ref = allocate(line, vec![&medium, &earliest, &latest]);
        assert_eq!(Ok("speedy-batch".to_owned()), batch_ref);

        assert_eq!(90, earliest.available_quantity());
        assert_eq!(100, medium.available_quantity());
        assert_eq!(100, latest.available_quantity());
    }
    
    #[test]
    fn test_raise_error() {
        let today = Utc::today();
        let batch = make_batch("batch1", "SMALL-FORK", 10, Some(today));
        let line = make_line("order-001", "SMALL-FORK", 10);

        allocate(make_line("order1", "SMALL-FORK", 10), vec![ &batch ]);
        assert_eq!(0, batch.available_quantity());        
        assert!(!batch.can_allocate(&line));
        
        let result  = allocate(make_line("order2", "SMALL-FORK", 1), vec![ &batch ]);
        
        assert_eq!(Err(OutOfStock), result);
    }
}
