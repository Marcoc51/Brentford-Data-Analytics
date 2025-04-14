WITH positions_raw AS (
    SELECT 
        TRIM(position.value::STRING) AS position
    FROM 
        {{ source('bronze', 'stg_Standard_Stats') }},
        LATERAL FLATTEN(input => SPLIT(pos, ',')) AS position
),

positions AS (
    SELECT DISTINCT position FROM positions_raw
)

SELECT 
    ROW_NUMBER() OVER (ORDER BY position) AS position_id
    ,position
    ,CURRENT_TIMESTAMP AS loaded_at
FROM 
    positions
