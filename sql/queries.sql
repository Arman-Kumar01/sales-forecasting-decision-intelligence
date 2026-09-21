-- Example of advanced analytical SQL used in this project
-- YoY Growth using Window Functions
WITH Monthly AS (
    SELECT strftime('%Y-%m', Order_Date) as YM, SUM(Sales) as Rev
    FROM orders GROUP BY 1
)
SELECT YM, Rev, LAG(Rev, 12) OVER(ORDER BY YM) as LastYearRev
FROM Monthly;
