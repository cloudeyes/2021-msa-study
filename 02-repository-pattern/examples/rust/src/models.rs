use chrono::{NaiveDate};
use super::schema::{batch, allocation};
use std::cmp::Ordering;


#[derive(Queryable, Default)]
pub struct Batch {
    pub id: Option<i32>,
    pub reference: String, 
    pub sku: String,
    pub eta: Option<NaiveDate>,
    pub _purchased_quantity: i32, 
}

#[derive(Queryable, PartialEq, Eq, Clone)]
pub struct OrderLine {
    pub id: Option<i32>,
    pub reference: String,
    pub sku: String,
    pub qty: i64,
    allocations: Vec<OrderLine>
}



impl Eq for Batch {}

// For entity's identity equality
impl PartialEq for Batch {
    fn eq(&self, other: &Self) -> bool {
        &self.reference == &other.reference
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

// For custom ordering
impl PartialOrd for Batch {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

#[derive(Insertable)]
#[table_name="batch"]
pub struct NewBatch<'a> {
    pub reference: &'a str,
    pub sku: &'a str,
pub _purchased_quantity: i32,
}


#[derive(Queryable, Associations)]
#[belongs_to(Batch)]
#[belongs_to(OrderLine)]
#[table_name = "allocation"]
pub struct Allocation {
    pub order_line_id: i32,
    pub batch_id: i32,
}
