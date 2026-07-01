CREATE TABLE IF NOT EXISTS dwd_orders AS
SELECT
    order_id,
    user_id,
    DATE(order_time) AS order_date,
    amount,
    status
FROM ods_orders
WHERE status = 'completed';
