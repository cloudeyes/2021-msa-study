table! {
    allocation (order_line_id, batch_id) {
        order_line_id -> Integer,
        batch_id -> Integer,
    }
}

table! {
    batch (id) {
        id -> Nullable<Integer>,
        reference -> Text,
        sku -> Text,
        eta -> Nullable<Date>,
        _purchased_quantity -> Integer,
    }
}

table! {
    order (id) {
        id -> Nullable<Integer>,
    }
}

table! {
    order_line (id) {
        id -> Nullable<Integer>,
        sku -> Text,
        qty -> Integer,
        orderid -> Integer,
    }
}

joinable!(allocation -> batch (batch_id));
joinable!(allocation -> order_line (order_line_id));
joinable!(order_line -> order (orderid));

allow_tables_to_appear_in_same_query!(
    allocation,
    batch,
    order,
    order_line,
);
