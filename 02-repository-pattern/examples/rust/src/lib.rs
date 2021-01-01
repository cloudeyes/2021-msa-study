#[macro_use]
extern crate diesel;
extern crate dotenv;

use diesel::prelude::*;
use diesel::sqlite::SqliteConnection;
use dotenv::dotenv;
use std::env;

pub mod models;
pub mod schema;

pub fn establish_connection() -> SqliteConnection {
    dotenv().ok();

let database_url = env::var("DATABASE_URL")
    .expect("DATABASE_URL must be set");

SqliteConnection::establish(&database_url)
    .expect(&format!("Error connecting to {}", database_url))
}


#[cfg(test)]
mod tests {
use super::*;
    use models::{Batch, NewBatch};
    use std::panic;

    fn run_test<F>(testfn: F) 
       where F: Fn(&SqliteConnection) -> () + panic::UnwindSafe
    {
        let conn = establish_connection();
        let result = panic::catch_unwind(move || {
            setup(&conn);
            testfn(&conn)
        });
        let conn2 = establish_connection();
        teardown(&conn2);
        assert!(result.is_ok())
    }

    fn create_batch<'a>(conn: &SqliteConnection, reference: &str, sku: &str, qty: i32) -> usize {
        use schema::batch;
        let new_batch = NewBatch {
            reference: reference, 
            sku: sku, 
            _purchased_quantity: qty, 
        };

        diesel::insert_into(batch::table)
            .values(&new_batch)
            .execute(conn)
            .expect("Error saving new batch")
    }

    fn clear_batch(conn: &SqliteConnection) -> () {
        let _ = diesel::sql_query("DELETE FROM batch")
            .execute(conn);
    }

    fn setup(conn: &SqliteConnection) {
        create_batch(conn, "batch-001", "TEST-TABLE", 30);
    }

    fn teardown(conn: &SqliteConnection) {
        clear_batch(conn);
    }

    #[test]
    fn get_models() {
        use schema::batch::dsl::*;
        run_test(|conn| {
            let results = batch.filter(reference.eq("batch-001".to_owned()))
                .limit(5)
                .load::<Batch>(conn)
                .expect("Error loading posts");

            assert_eq!(1, results.len());

            let b1 = results.first().unwrap();
            assert_eq!("batch-001", b1.reference);
            assert_eq!("TEST-TABLE", b1.sku);
        })
    }


    //#[test]
    //fn orderline_mapper_can_load_lines() {
    //}

}
