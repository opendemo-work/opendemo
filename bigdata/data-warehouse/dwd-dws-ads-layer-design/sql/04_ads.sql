CREATE TABLE IF NOT EXISTS ads_user_summary AS
SELECT
    user_id,
    SUM(order_cnt) AS total_orders,
    SUM(total_amount) AS total_amount
FROM dws_user_daily
GROUP BY user_id;
