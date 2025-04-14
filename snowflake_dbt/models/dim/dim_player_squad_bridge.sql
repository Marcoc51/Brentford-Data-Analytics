SELECT 
    p.player_id,
    sq.squad_id,
    CURRENT_TIMESTAMP AS loaded_at
FROM 
    {{ ref('dim_players') }} AS p
JOIN 
    {{ source('bronze', 'stg_Standard_Stats') }} AS s
ON
    s.player = p.player_name
JOIN 
    {{ ref('dim_squads') }} AS sq
ON 
    s.squad = sq.squad_name