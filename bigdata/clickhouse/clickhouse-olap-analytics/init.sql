CREATE DATABASE IF NOT EXISTS demo;

CREATE TABLE IF NOT EXISTS demo.events (
    event_date Date,
    user_id UInt64,
    event_type String,
    amount Decimal64(2)
) ENGINE = MergeTree()
ORDER BY (event_date, user_id);

INSERT INTO demo.events VALUES
('2026-06-01', 1, 'purchase', 100.00),
('2026-06-01', 2, 'view', 0.00),
('2026-06-02', 1, 'purchase', 250.00),
('2026-06-02', 3, 'purchase', 80.00);
