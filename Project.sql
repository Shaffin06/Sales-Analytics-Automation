CREATE TABLE customers (
    customer_id NUMBER PRIMARY KEY,
    name VARCHAR2(100),
    city VARCHAR2(100),
    signup_date DATE
);
CREATE TABLE products (
    product_id NUMBER PRIMARY KEY,
    name VARCHAR2(100),
    price NUMBER(10,2)
);
CREATE TABLE orders (
    order_id NUMBER PRIMARY KEY,
    customer_id NUMBER,
    order_date DATE,
    total_amount NUMBER(12,2),
    status VARCHAR2(30),
    CONSTRAINT fk_orders_customers FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);
CREATE TABLE order_items (
    id NUMBER PRIMARY KEY,
    order_id NUMBER,
    product_id NUMBER,
    qty NUMBER,
    price_each NUMBER(10,2),
    CONSTRAINT fk_items_orders FOREIGN KEY(order_id) REFERENCES orders(order_id),
    CONSTRAINT fk_items_products FOREIGN KEY(product_id) REFERENCES products(product_id)
);

INSERT INTO customers VALUES(1,'Amit Kumar','Chennai', DATE '2024-10-10');
INSERT INTO customers VALUES(2,'Priya Sharma','Bengaluru', DATE '2024-11-01');
INSERT INTO customers VALUES(3,'Ravi Singh','Mumbai', DATE '2024-11-12');
INSERT INTO customers VALUES(4,'Sara Das','Chennai', DATE '2024-12-02');
INSERT INTO customers VALUES(5,'Nikhil Rao','Hyderabad', DATE '2024-09-13');
INSERT INTO customers VALUES(6,'Maya Patel','Delhi', DATE '2024-11-25');

INSERT INTO products VALUES(1,'Widget A',499.00);
INSERT INTO products VALUES(2,'Widget B',999.00);
INSERT INTO products VALUES(3,'Gadget C',1499.00);

INSERT INTO orders VALUES(1001,1, DATE '2025-03-01', 1498.00, 'completed');
INSERT INTO orders VALUES(1002,2, DATE '2025-03-01', 999.00, 'completed');
INSERT INTO orders VALUES(1003,3, DATE '2025-03-02', 199.00, 'completed');
INSERT INTO orders VALUES(1004,4, DATE '2025-03-02', 499.00, 'completed');
INSERT INTO orders VALUES(1005,5, DATE '2025-03-03', 2499.00, 'completed');
INSERT INTO orders VALUES(1006,6, DATE '2025-03-03', 1498.00, 'completed');
INSERT INTO orders VALUES(1007,1, DATE '2025-03-04', 2498.00, 'completed');

INSERT INTO order_items VALUES(1,1001,1,1,499.00);
INSERT INTO order_items VALUES(2,1001,2,1,999.00);
INSERT INTO order_items VALUES(3,1002,2,1,999.00);
INSERT INTO order_items VALUES(4,1003,3,1,199.00);
INSERT INTO order_items VALUES(5,1004,1,1,499.00);
INSERT INTO order_items VALUES(6,1005,3,1,2499.00);
INSERT INTO order_items VALUES(7,1006,1,2,499.00);
INSERT INTO order_items VALUES(8,1007,3,1,1499.00);
INSERT INTO order_items VALUES(9,1007,2,1,999.00);
COMMIT;


select * from customers order by customer_id;
select * from orders;
select * from order_items;

