from functions.scrape_data import scrape_tables
from functions.clean_data import flatten_columns, clean_table, insert_squad_column
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Load .env from the project root
sys.path.append(str(Path(__file__).resolve().parents[1] / 'scripts'))
env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

# Now use environment variables
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = "localhost"
DB_PORT = os.getenv("HOST_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

# Create database engine
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Define the XPATH for the Championship table
championship_xpath = '/html/body/div[4]/div[6]/div[3]/div[4]/table'

# URLs to scrape
urls = {
    "Standard_Stats": "https://fbref.com/en/comps/10/stats/Championship-Stats",
    "Goalkeeping": "https://fbref.com/en/comps/10/keepers/Championship-Stats",
    "Advanced_Goalkeeping": "https://fbref.com/en/comps/10/keepersadv/Championship-Stats",
    "Shooting": "https://fbref.com/en/comps/10/shooting/Championship-Stats",
    "Passing": "https://fbref.com/en/comps/10/passing/Championship-Stats",
    "Pass_Types": "https://fbref.com/en/comps/10/passing_types/Championship-Stats",
    "Goal_Shot_Creation": "https://fbref.com/en/comps/10/gca/Championship-Stats",
    "Defensive_Actions": "https://fbref.com/en/comps/10/defense/Championship-Stats",
    "Possession": "https://fbref.com/en/comps/10/possession/Championship-Stats",
    "Playing_Time": "https://fbref.com/en/comps/10/playingtime/Championship-Stats",
    "Miscellaneous_Stats": "https://fbref.com/en/comps/10/misc/Championship-Stats",
    "Brentford": "https://fbref.com/en/squads/cd051869/2024-2025/c9/Brentford-Stats-Premier-League"
}

tables_names = [
    'Standard_Stats',
    'Scores_Fixtures',
    'Goalkeeping',
    'Advanced_Goalkeeping',
    'Shooting',
    'Passing',
    'Pass_Types',
    'Goal_Shot_Creation',
    'Defensive_Actions',
    'Possession',
    'Playing_Time',
    'Miscellaneous_Stats'
]

with engine.begin() as conn:
    for tbl in tables_names:
        table_name = f"stg_{tbl}"
        conn.execute(text(f'DROP TABLE IF EXISTS "public"."{table_name}";'))
    print("✅ Truncated all existing tables.")

# Scrape and explore data
for name, url in urls.items():
    if name == "Brentford":
        tables = scrape_tables(url=url, club=name)

        if tables:
            print("-" * 20)
            print(len(tables), "tables found")
        
            # Only take the first 12 tables
            for i, table in enumerate(tables[9:21]):
                # Claen and flatten the table
                table = flatten_columns(table)
                table = clean_table(club=name, table=table)

                # Insert the squad column for Brentford
                table = insert_squad_column(table, squad_name="Brentford")

                # Get the table name
                table_name = f"stg_{tables_names[i]}"

                # Store the table in the database
                table.to_sql(table_name, engine, schema="public", if_exists='append', index=False)
                
                print("-" * 20)
                print(f'✅ Loaded Brentford "{tables_names[i]}" data into "{table_name}"')
    else:
        table = scrape_tables(url=url, club=name, xpath=championship_xpath)

        # Check if the table is empty
        if table.empty:
            print("-" * 20)
            print(f"❌ No tables found for {name}")
            continue

        print("-" * 20)
        print(f"Found the table for the Championship's players \"{name}\" data")

        # Claen and flatten the table
        table = flatten_columns(table)
        table = clean_table(club=name, table=table)

        # Get the table name
        table_name = f"stg_{name}"
        
        # Store the table in the database
        table.to_sql(table_name, engine, schema="public", if_exists='append', index=False)

        print(f"✅ Loaded Championship's players \"{name}\" data into \"{table_name}\"")

# Finish the scraping process
print("-" * 20)
print("🏁 Data exploration and loading completed.")
