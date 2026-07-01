CREATE TABLE IF NOT EXISTS ods_orders (
    order_id BIGINT,
    user_id BIGINT,
    order_time DATETIME,
    amount DECIMAL(10,2),
    status VARCHAR(50)
);

INSERT INTO ods_orders VALUES
(1, 1001, '2026-06-01 10:00:00', 120.00, 'completed'),
(2, 1002, '2026-06-01 11:00:00', 300.00, 'completed'),
(3, 1001, '2026-06-02 09:00:00', 80.00, 'pending');
