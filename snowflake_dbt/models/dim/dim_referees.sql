SELECT 
    ROW_NUMBER() OVER (ORDER BY referee) AS referee_id,
    referee AS referee_name,
    CURRENT_TIMESTAMP AS loaded_at
FROM 
    {{ source('bronze', 'stg_Scores_Fixtures') }}
WHERE 
    referee IS NOT NULL
GROUP BY 
    referee