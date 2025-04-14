# 📚 Data Dictionary - Brentford Data Analytics

This document describes the tables and fields used in the **Silver layer** of the Brentford Data Analytics project.

---

## 📁 Dimension Tables

### `dim_players`
| Column        | Description                                 |
|---------------|---------------------------------------------|
| `player_id`   | **PK.** Unique identifier for each player   |
| `player_name` | Full name of the player                     |
| `nationality` | Country of nationality                      |
| `birthdate`   | Estimated birthdate calculated from age     |
| `loaded_at`   | Timestamp of when the record was loaded     |

---

### `dim_squads`
| Column        | Description                          |
|---------------|--------------------------------------|
| `squad_id`    | **PK.** Unique identifier for squad  |
| `squad_name`  | Name of the team                     |
| `loaded_at`   | Timestamp of when the record was loaded |

---

### `dim_positions`
| Column        | Description                            |
|---------------|----------------------------------------|
| `position_id` | **PK.** Unique identifier for position |
| `position`    | Position code (e.g., FWD, MID, DEF)    |
| `loaded_at`   | Timestamp of when the record was loaded |

---

### `dim_referees`
| Column        | Description                              |
|---------------|------------------------------------------|
| `referee_id`  | **PK.** Unique identifier for referee     |
| `referee_name`| Full name of the referee                  |
| `loaded_at`   | Timestamp of when the record was loaded   |

---

### `dim_matches`
| Column              | Description                                             |
|---------------------|---------------------------------------------------------|
| `match_id`          | **PK.** Unique identifier for the match                 |
| `match_date_id`     | **FK.** Links to `dim_date_time`                        |
| `match_venue`       | Venue of the match                                      |
| `match_result`      | Final result (e.g., W, L, D)                             |
| `opponent_team`     | Opponent team name                                      |
| `captain_id`        | **FK.** Links to `dim_players`                          |
| `match_referee`     | **FK.** Links to `dim_referees`                         |
| `formation`         | Team formation used                                     |
| `opponent_formation`| Opponent formation used                                 |
| `loaded_at`         | Timestamp of when the record was loaded                 |

---

### `dim_date_time`
| Column           | Description                                        |
|------------------|----------------------------------------------------|
| `date_time_id`   | **PK.** Unique identifier for date-hour pair       |
| `datetime`       | Combined datetime (timestamp)                      |
| `date`           | Date only (YYYY-MM-DD)                             |
| `hour`           | Hour of the day (0–23)                             |
| `year`           | Year                                               |
| `month`          | Month                                              |
| `day`            | Day of month                                       |
| `weekday_name`   | Full weekday name (e.g., Monday)                   |
| `weekday_short`  | Abbreviation (e.g., Mon)                           |
| `week_of_year`   | Week number                                        |
| `quarter`        | Quarter of the year (1–4)                          |
| `weekday_type`   | Weekday or Weekend                                 |
| `loaded_at`      | Timestamp of when the record was loaded            |

---

## 🔷 Bridge Tables

### `dim_player_position_bridge`
| Column        | Description                          |
|---------------|--------------------------------------|
| `player_id`   | **FK.** Links to `dim_players`       |
| `position_id` | **FK.** Links to `dim_positions`     |
| `loaded_at`   | Timestamp of when the record was loaded |

---

### `dim_player_squad_bridge`
| Column        | Description                          |
|---------------|--------------------------------------|
| `player_id`   | **FK.** Links to `dim_players`       |
| `squad_id`    | **FK.** Links to `dim_squads`        |
| `loaded_at`   | Timestamp of when the record was loaded |

---

## 🧮 Fact Tables

### `fact_players`
| Column            | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `fact_player_id`  | **PK.** Hashed key of player-squad row                       |
| `player_id`       | **FK.** Links to `dim_players`                               |
| `squad_id`        | **FK.** Links to `dim_squads`                                |
| ...               | Metrics on player stats: playing time, shooting, passing, xG |
| `loaded_at`       | Timestamp of when the record was loaded                      |

🔎 **Grain**: One record per player per squad

---

### `fact_goalkeeping`
| Column                | Description                                               |
|------------------------|-----------------------------------------------------------|
| `fact_goalkeeping_id`  | **PK.** Hashed key of player-squad-performance combo      |
| `player_id`            | **FK.** Links to `dim_players`                            |
| `squad_id`             | **FK.** Links to `dim_squads`                             |
| ...                    | Metrics: saves, xG on target, clean sheets, sweeping      |
| `loaded_at`            | Timestamp of when the record was loaded                   |

🔎 **Grain**: One record per goalkeeper per squad

---

### `fact_matches`
| Column        | Description                                |
|---------------|--------------------------------------------|
| `match_id`    | **FK.** Links to `dim_matches`             |
| `goals_for`   | Goals scored                               |
| `goals_against`| Goals conceded                            |
| `xg_for`      | Expected goals for                         |
| `xg_against`  | Expected goals against                     |
| `result`      | W / L / D result                           |
| `loaded_at`   | Timestamp of when the record was loaded    |

🔎 **Grain**: One record per match

---

📌 **Note**: All models include a `loaded_at` timestamp to track the latest refresh time of each row.
