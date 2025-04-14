WITH date_range AS (
    SELECT
        DATEADD(DAY, SEQ4(), '2022-01-01') AS base_date
    FROM TABLE(GENERATOR(ROWCOUNT => 1825))  -- 5 years * 365 days
),
hour_range AS (
    SELECT SEQ4() AS hour
    FROM TABLE(GENERATOR(ROWCOUNT => 24))
),
date_hour_range AS (
    SELECT 
        d.base_date,
        h.hour
    FROM date_range d
    CROSS JOIN hour_range h
)

SELECT 
    ROW_NUMBER() OVER (ORDER BY base_date, hour) AS date_time_id
    ,DATEADD(HOUR, hour, base_date) AS datetime
    ,hour
    ,CAST(base_date AS DATE) AS date
    ,YEAR(base_date) AS year
    ,MONTH(base_date) AS month
    ,DAY(base_date) AS day
    ,TO_CHAR(base_date, 'DY') AS weekday_short
    ,WEEK(base_date) AS week_of_year
    ,QUARTER(base_date) AS quarter
    ,CASE 
        WHEN DATE_PART(DOW, base_date) IN (0, 6) THEN 'Weekend'
        ELSE 'Weekday'
    END AS weekday_type
    ,CURRENT_TIMESTAMP AS loaded_at
FROM date_hour_range
