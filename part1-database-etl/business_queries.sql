-- Query 1: Customer Purchase History
-- Shows customers with at least 2 orders and total spend > 5000

SELECT 
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.quantity * oi.unit_price) AS total_spent
FROM customers c
JOIN orders o 
    ON c.customer_id = o.customer_id
JOIN order_items oi 
    ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.email
HAVING COUNT(DISTINCT o.order_id) >= 2
   AND SUM(oi.quantity * oi.unit_price) > 5000
ORDER BY total_spent DESC;


-- Query 2: Product Sales Analysis
-- Shows categories with revenue greater than 10000
SELECT
    p.category,
    COUNT(DISTINCT p.product_id) AS num_products,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY p.category
HAVING SUM(oi.quantity * oi.unit_price) > 10000
ORDER BY total_revenue DESC;


-- Query 3: Monthly Sales Trend for 2024
-- Shows monthly revenue and cumulative revenue

SELECT
    MONTHNAME(o.order_date) AS month_name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.quantity * oi.unit_price) AS monthly_revenue,
    SUM(SUM(oi.quantity * oi.unit_price)) OVER (
        ORDER BY MONTH(o.order_date)
    ) AS cumulative_revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE YEAR(o.order_date) = 2024
GROUP BY MONTH(o.order_date), MONTHNAME(o.order_date)
ORDER BY MONTH(o.order_date);



