CREATE TABLE IF NOT EXISTS dws_user_daily AS
SELECT
    user_id,
    order_date,
    COUNT(order_id) AS order_cnt,
    SUM(amount) AS total_amount
FROM dwd_orders
GROUP BY user_id, order_date;
