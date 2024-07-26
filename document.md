# Steps:
* `pip install streamlit sqlalchemy snowflake-sqlalchemy pandas openai`
* `streamlit run frosty_app.py`

# Chosen Queries
* **Query2** Report the increase of weekly web and catalog sales from one year to the next year for each week.  That is, compute the increase of Monday, Tuesday, ... Sunday sales from one year to the following. Qualification Substitution Parameters: 
    * YEAR.01=2001 

```USE DATABASE SNOWFLAKE_SAMPLE_DATA;

WITH current_year_sales AS (
    SELECT DATE_PART(WEEKDAY, dd.D_DATE) AS day_of_week, dd.D_WEEK_SEQ,
           SUM(ws.WS_EXT_SALES_PRICE) AS current_year_sales
    FROM TPCDS_SF10TCL.WEB_SALES ws
    JOIN TPCDS_SF10TCL.DATE_DIM dd ON ws.WS_SOLD_DATE_SK = dd.D_DATE_SK
    WHERE dd.D_YEAR = 2001
    GROUP BY day_of_week, dd.D_WEEK_SEQ
),
next_year_sales AS (
    SELECT DATE_PART(WEEKDAY, dd.D_DATE) AS day_of_week, dd.D_WEEK_SEQ,
           SUM(ws.WS_EXT_SALES_PRICE) AS next_year_sales
    FROM TPCDS_SF10TCL.WEB_SALES ws
    JOIN TPCDS_SF10TCL.DATE_DIM dd ON ws.WS_SOLD_DATE_SK = dd.D_DATE_SK
    WHERE dd.D_YEAR = 2002
    GROUP BY day_of_week, dd.D_WEEK_SEQ
)
SELECT cys.day_of_week, cys.D_WEEK_SEQ, 
       cys.current_year_sales AS current_year_sales,
       nys.next_year_sales AS next_year_sales,
       (nys.next_year_sales - cys.current_year_sales) AS sales_increase
FROM current_year_sales cys
JOIN next_year_sales nys ON cys.day_of_week = nys.day_of_week;
```

* **Query24**: Calculates the total monetary value of items in specific colors for store sales transactions, listing customers whose total specified value is a certain percentage above the average .

* **Query27**: For all items sold in stores located in six states during a given year, finds the average quantity, list price, sales price, and average coupon amount by demographic attributes .

* **Query40**: Analyzes the impact of item price changes on sales by computing total sales for items before and after the price change, grouped by warehouse location .

* **Query43**: Reports the sum of all sales from Sunday to Saturday for stores within a specified date range .

* **Query45**: Lists the best and worst-performing products measured by net profit .

* **Query55**: Compares sales data across different periods and channels to identify trends and anomalies .

* **Query70**: Calculates net profit for items sold through various channels, aggregating results by item and store .

* **Query77**: Analyzes customer demographics and purchase patterns to improve marketing strategies .

* **Query80**: Evaluates the effectiveness of promotional campaigns by analyzing sales data before, during, and after promotions .