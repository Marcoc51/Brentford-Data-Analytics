SELECT 
    ROW_NUMBER() OVER (ORDER BY m.date) AS match_id
    ,t.date_time_id AS match_date_id 
    ,m.venue AS match_venue
    ,m.result AS match_result
    ,m.opponent AS opponent_team
    ,p.player_id AS captain_id
    ,m.formation
    ,m.opp_formation AS opponent_formation
    ,r.referee_id AS match_referee
    ,CURRENT_TIMESTAMP AS loaded_at
FROM 
    {{ source('bronze', 'stg_Scores_Fixtures') }} AS m
JOIN 
    {{ ref('dim_players') }} AS p
ON 
    p.player_name = m.captain
JOIN 
    {{ ref('dim_referees') }} AS r
ON
    r.referee_name = m.referee
JOIN 
    {{ ref('dim_date_time') }} AS t
ON
    t.datetime = TRY_TO_TIMESTAMP(m.date || ' ' || SPLIT_PART(m.time, ' ', 1))
WHERE 
    result IS NOT NULL