CREATE TABLE "order" (
id INTEGER PRIMARY KEY AUTOINCREMENT 
); 

CREATE TABLE batch (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    reference VARCHAR(255) NOT NULL, 
    sku VARCHAR(255) NOT NULL, 
    eta DATE,
    _purchased_quantity INTEGER NOT NULL, 
    UNIQUE (reference)
);

CREATE TABLE order_line (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    sku VARCHAR(255) NOT NULL, 
    qty INTEGER NOT NULL, 
    orderid INTEGER NOT NULL, 
    FOREIGN KEY(orderid) REFERENCES "order" (id)
); 

CREATE TABLE allocation (
    order_line_id INTEGER NOT NULL, 
    batch_id INTEGER NOT NULL, 
    PRIMARY KEY (order_line_id, batch_id),
    FOREIGN KEY(order_line_id) REFERENCES order_line (id), 
    FOREIGN KEY(batch_id) REFERENCES batch (id)
);
