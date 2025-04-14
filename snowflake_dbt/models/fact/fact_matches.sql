SELECT 
    ROW_NUMBER() OVER (ORDER BY m.date) AS match_id
    ,m.gf
    ,m.ga
    ,m.xg
    ,m.xga
    ,m.poss
    ,m.attendance
    ,CURRENT_TIMESTAMP AS loaded_at

FROM 
    {{ source('bronze', 'stg_Scores_Fixtures') }} AS m