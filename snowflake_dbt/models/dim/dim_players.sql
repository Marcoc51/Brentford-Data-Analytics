WITH ranked_players AS (
    SELECT
        p.player
        ,SPLIT_PART(p.nation, ' ', 2) AS nationality
        ,DATEADD(
            DAY,
            -TRY_CAST(SPLIT_PART(p.age, '-', 2) AS INT),
            DATEADD(
                YEAR,
                -TRY_CAST(SPLIT_PART(p.age, '-', 1) AS INT),
                CURRENT_DATE
            )
        ) AS birthdate
        ,CURRENT_TIMESTAMP AS loaded_at
        ,ROW_NUMBER() OVER (PARTITION BY p.player ORDER BY p.player) AS rn
    FROM 
        {{ source('bronze', 'stg_Standard_Stats') }} AS p
)

SELECT
    ROW_NUMBER() OVER (ORDER BY player) AS player_id,
    player AS player_name,
    nationality,
    birthdate,
    loaded_at
FROM 
    ranked_players
WHERE rn = 1
