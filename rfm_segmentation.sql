/* Dataset: Superstore Sales Data
 
Task:
CREATE A DATABASE IN MYSQL
CREATE A TABLE UNDER THAT DATABASE
INSERT THE ATTACH DATA THERE (PREFERABLY BULK INSERTION)
EXPLORE THE DATA AND CHECK IF ALL THE DATA IS IN THE PROPER FORMAT
DO THE NECESSARY CLEANING AND UPDATE THE TABLE SCHEMA IF REQUIRED
PERFORM EXPLORATORY DATA ANALYSIS
SEGMENT THE CUSTOMER USING RFM SEGMENTATION
*** PRESENT YOUR FINDINGS IN A GITHUB REPOSITORY LIKE WE DISCUSSED
*** MAKE IT A PUBLIC REPO AND SHARE THE LINK HERE
*/

-- whole data
select * from superstore_sales_data limit 10;

-- Explore Columns
describe superstore_sales_data;

 -- Check for Missing Values
SELECT
    SUM(CASE WHEN Row_ID IS NULL THEN 1 ELSE 0 END) AS Rowid,
    SUM(CASE WHEN Customer_ID IS NULL THEN 1 ELSE 0 END) AS Customers,
    SUM(CASE WHEN  Order_Date IS NULL THEN 1 ELSE 0 END) AS OrderDate,
	SUM(CASE WHEN  Return_Status IS NULL THEN 1 ELSE 0 END) AS ReturnStatus,
    SUM(CASE WHEN  Order_Date IS NULL THEN 1 ELSE 0 END) AS orderdate,
    SUM(CASE WHEN  Customer_Name IS NULL THEN 1 ELSE 0 END) AS Name
FROM superstore_sales_data;

-- Check unipue values
select distinct row_id from superstore_sales_data;
select distinct unit_price from superstore_sales_data;
select distinct customer_id from superstore_sales_data;
select distinct Customer_Name from superstore_sales_data;
select distinct Product_Name from superstore_sales_data;
select distinct Region from superstore_sales_data;
select distinct City from superstore_sales_data;
select distinct quantity_ordered_new from superstore_sales_data;

-- profit by manager
select  manager, 
       round(sum(sales),0) as profit
from superstore_sales_data
group by 1;

-- city & Region wise sale 
select city,
	   Region,
    round(sum(sales),0) as total_sales
from superstore_sales_data
group by city,Region;

-- last transaction date & First transaction date.
SELECT  Customer_ID, 
	   MIN(STR_TO_DATE(Order_Date, '%m/%d/%Y')) AS last_purchase_date ,  
       MAX(STR_TO_DATE(Order_Date, '%m/%d/%Y')) AS first_purchase_date  
FROM superstore_sales_data 
group by Customer_ID;

-- RFM segmentation the customers segmenttion With R(Recency), F(Frequency), M(Monetary)

CREATE OR REPLACE VIEW RFM_SCORE_DATA AS
with RFM_Values as
(
select customer_name,
     datediff(
     (select MAX(STR_TO_DATE(Order_Date, '%m/%d/%Y')) FROM superstore_sales_data), 
        MAX(STR_TO_DATE(Order_Date, '%m/%d/%Y'))
     ) as Recency_value,
     count(distinct order_id) as Frequency_value,
     round(sum(Sales)) as Monetary_value
from superstore_sales_data
group by customer_name),

-- RFM scoring 
RFM_Scrore as 
(select 
     c.*,
     NTILE (4) over (order by Recency_value DESC ) as R_score,
     NTILE (4) over (order by Frequency_value ASC ) as F_score,
     NTILE (4) over (order by Monetary_Value ASC ) as M_score
from RFM_Values as C)

select 
    R.*,
    (R_score + F_score + M_score) as Total_RFM_Score,
    concat_ws('',R_score,F_score,M_score) as RFM_Combination 
from RFM_Scrore as R;

CREATE OR REPLACE VIEW RFM_ANALYSIS AS
select 
 RFM_SCORE_DATA .*,
   case 
        WHEN RFM_Combination IN (111, 112, 121, 132, 211, 211, 212, 114, 141) THEN 'CHURNED CUSTOMER'
        WHEN RFM_Combination IN (133, 134, 143, 224, 334, 343, 344, 144) THEN 'SLIPPING AWAY, CANNOT LOSE'
        WHEN RFM_Combination IN (311, 411, 331) THEN 'NEW CUSTOMERS'
        WHEN RFM_Combination IN (222, 231, 221,  223, 233, 322) THEN 'POTENTIAL CHURNERS'
        WHEN RFM_Combination IN (323, 333,321, 341, 422, 332, 432) THEN 'ACTIVE'
        WHEN RFM_Combination IN (433, 434, 443, 444) THEN 'LOYAL'
    ELSE 'Other'
    END AS CUSTOMER_SEGMENT
FROM RFM_SCORE_DATA;

select CUSTOMER_SEGMENT,
      count(*) as Number_of_Customers,
      round(avg(Monetary_value),0) as Monetary_avg_Value
from rfm_analysis
group by Customer_segment; 
