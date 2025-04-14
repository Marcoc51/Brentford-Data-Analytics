SELECT
    md5(
        COALESCE(CAST(p.player_id AS STRING), '') || 
        COALESCE(CAST(s.squad_id AS STRING), '') || 
        COALESCE(CAST(ga.playing_time_min AS STRING), '')
    ) AS fact_goalkeeping_id
    
    -- Dim references
    ,p.player_id
    ,s.squad_id

    -- Standard Goalkeeping Metrics
    ,ga.penalty_kicks_pka
    ,ga.penalty_kicks_pkatt
    ,ga.penalty_kicks_pkm
    ,ga.penalty_kicks_pksv
    ,ga.penalty_kicks_savex AS penalty_kicks_save_pct
    ,ga.performance_cs
    ,ga.performance_csx  AS performance_cs_pct
    ,ga.performance_d
    ,ga.performance_ga
    ,ga.performance_ga90 AS performance_ga_per_90
    ,ga.performance_l
    ,ga.performance_savex AS performance_save_pct
    ,ga.performance_saves
    ,ga.performance_sota
    ,ga.performance_w
    ,ga.playing_time_90s
    ,ga.playing_time_min
    ,ga.playing_time_mp
    ,ga.playing_time_starts
    
    -- Advanced Goalkeeping Metrics
    ,ga_a.crosses_opp
    ,ga_a.crosses_stp
    ,ga_a.crosses_stpx AS crosses_stp_pct
    ,ga_a.expected_90 AS expected_per_90
    ,ga_a.expected_psxg
    ,ga_a.expected_psxgxxx AS expected_psxg_plus_minus
    ,ga_a.expected_psxg_sot AS expected_psxg_per_sot
    ,ga_a.goal_kicks_att
    ,ga_a.goal_kicks_avglen
    ,ga_a.goal_kicks_launchx AS goal_kicks_launch_pct
    ,ga_a.goals_ck
    ,ga_a.goals_fk
    ,ga_a.goals_ga
    ,ga_a.goals_og
    ,ga_a.goals_pka
    ,ga_a.launched_att
    ,ga_a.launched_cmp
    ,ga_a.launched_cmpx AS launched_cmp_pct
    ,ga_a.passes_att_gkx AS passes_att_gk
    ,ga_a.passes_avglen
    ,ga_a.passes_launchx AS passes_launch_pct
    ,ga_a.passes_thr
    ,ga_a.sweeper_opa AS sweeper_opa
    ,ga_a.sweeper_opa_90 AS sweeper_opa_per_90
    ,ga_a.sweeper_avgdist
    ,CURRENT_TIMESTAMP AS loaded_at
FROM 
    {{ source('bronze', 'stg_Goalkeeping') }} AS ga
LEFT JOIN 
    {{ source('bronze', 'stg_Advanced_Goalkeeping') }} AS ga_a
ON 
    ga.player = ga_a.player 
AND 
    ga.squad = ga_a.squad
LEFT JOIN 
    {{ ref('dim_players') }} AS p
ON 
    ga.player = p.player_name
LEFT JOIN
    {{ ref('dim_squads') }} AS s
ON
    ga.squad = s.squad_name