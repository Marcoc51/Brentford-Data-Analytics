import pandas as pd

def flatten_columns(df):
    """
    Flattens multi-level column headers and cleans column names.
    Replaces spaces with underscores and removes 'Unnamed' levels.
    """
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            '_'.join([str(level).strip().replace(' ', '_') for level in col if 'Unnamed' not in str(level)]).strip('_')
            for col in df.columns
        ]
    else:
        df.columns = [
            str(col).strip().replace(' ', '_') for col in df.columns
        ]

    # Lowercase all column names
    df.columns = [col.lower() for col in df.columns]

    return df

def clean_table(club: str, table: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the Championship stats table:
    - Drops unnecessary columns if they exist (case-insensitive, space-insensitive)
    - Removes rows like 'Squad Total', 'Opponent Total', or 'Player' header rows
    """
    # Normalize column names for reliable matching
    normalized_columns = {col.lower().strip().replace(" ", "_"): col for col in table.columns}

    brentford_columns_to_drop_raw = ["matches", "match_report", "notes"]
    championship_columns_to_drop_raw = ["rk", "born", "matches"]

    if club == "Brentford":
        if "mp" in table.columns:
            table.rename(columns={"mp": "playing_time_mp"}, inplace=True)
        columns_to_drop_raw = brentford_columns_to_drop_raw
    else:
        columns_to_drop_raw = championship_columns_to_drop_raw
    
    columns_to_drop = [normalized_columns[col] for col in columns_to_drop_raw if col in normalized_columns]

    table.drop(columns=columns_to_drop, inplace=True)

    # Remove summary or duplicate header rows
    table = table[~table.apply(
        lambda row: row.astype(str).str.contains(
            "Squad Total|Opponent Total|Player|Per 90 Minutes|Time|Team Success \\(xG\\)", case=False
        ).any(), axis=1
    )]

    return table

def insert_squad_column(df: pd.DataFrame, squad_name: str = "Brentford") -> pd.DataFrame:
    """
    Inserts a 'squad' column with a fixed value after 'pos' and before 'age' columns if they exist.
    """
    # Ensure we're working on a copy of the DataFrame to avoid SettingWithCopyWarning
    df = df.copy()

    if 'pos' in df.columns and 'age' in df.columns:
        pos_index = df.columns.get_loc('pos')
        age_index = df.columns.get_loc('age')

        # Insert 'squad' between Pos and Age
        insert_at = min(age_index, pos_index) + 1
        df.insert(loc=insert_at, column='squad', value=squad_name)
    
    return df

def store_data(df, table_name, engine, schema="raw", if_exists="append"):
    """Store DataFrame into PostgreSQL."""
    df.to_sql(table_name, engine, schema=schema, if_exists=if_exists, index=False)
    print(f"✅ Stored {table_name} into schema '{schema}' with mode '{if_exists}'")