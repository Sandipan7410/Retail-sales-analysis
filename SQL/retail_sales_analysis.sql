-- 1. Top 10 Best-Selling Products by Revenue
SELECT 
    product_id,
    ROUND(SUM(sale_price), 2) AS sales
FROM df_orders
GROUP BY product_id
ORDER BY sales DESC
LIMIT 10;

-- 2. Category-wise Sales vs Profit Analysis
SELECT 
    category,
    ROUND(SUM(sale_price), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM df_orders
GROUP BY category
ORDER BY total_sales DESC;

-- 3. Top 5 Best-Selling Products Per Region (Window Function)
WITH regional_sales AS (
    SELECT 
        region,
        product_id,
        ROUND(SUM(sale_price), 2) AS sales
    FROM df_orders
    GROUP BY region, product_id
),
ranked_sales AS (
    SELECT 
        region,
        product_id,
        sales,
        ROW_NUMBER() OVER(PARTITION BY region ORDER BY sales DESC) AS rn
    FROM regional_sales
)
SELECT 
    region,
    product_id,
    sales,
    rn
FROM ranked_sales
WHERE rn <= 5;

-- 4. Monthly Revenue Trend
SELECT 
    strftime('%Y-%m-01', order_date) AS month,
    ROUND(SUM(sale_price), 2) AS monthly_sales
FROM df_orders
GROUP BY month
ORDER BY month;

-- 5. Most Ordered Sub-Categories by Quantity
SELECT 
    sub_category,
    SUM(quantity) AS total_quantity
FROM df_orders
GROUP BY sub_category
ORDER BY total_quantity DESC;

-- 6. Top 5 Cities by Total Sales
SELECT 
    city,
    ROUND(SUM(sale_price), 2) AS total_sales
FROM df_orders
GROUP BY city
ORDER BY total_sales DESC
LIMIT 5;
