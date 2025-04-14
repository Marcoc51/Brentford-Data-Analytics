WITH distinct_squads AS (
    SELECT 
        DISTINCT squad AS squad_name
    FROM 
        {{ source('bronze', 'stg_Standard_Stats') }}
)

SELECT
    row_number() over (order by squad_name) AS squad_id
    ,squad_name
    ,CASE 
        WHEN squad_name = 'Brentford' THEN 'Premier League'
        ELSE 'Championship'
    END AS league_name
    ,CURRENT_TIMESTAMP AS loaded_at
FROM 
    distinct_squads