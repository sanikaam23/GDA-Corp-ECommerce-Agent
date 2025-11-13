import pandas as pd
from sqlalchemy import create_engine, text
import os
import glob
from typing import Optional


DATA_DIR = 'data'
DB_NAME = 'olist_ecom.db'


def load_data_to_db(data_dir: str = DATA_DIR, db_name: str = DB_NAME) -> Optional[str]:
    """
    Loads all CSV files from the specified directory into a SQLite database.

    Args:
        data_dir: The directory containing the Olist CSV files.
        db_name: The name of the SQLite database file to create.

    Returns:
        The full file path to the created database, or None if loading fails.
    """

    db_path = os.path.join(os.getcwd(), db_name)
    engine = create_engine(f'sqlite:///{db_path}')


    csv_files = glob.glob(os.path.join(data_dir, '*.csv'))

    if not csv_files:
        print(f"❌ Error: No CSV files found in the '{data_dir}' directory.")
    
        raise FileNotFoundError(
            f"Missing Olist CSV files. Please place all 9 files into the '{data_dir}' folder."
        )

    print(f"--- Starting data load: {len(csv_files)} files found. ---")

    
    loaded_tables = []

    for file_path in csv_files:
        try:
            file_name = os.path.basename(file_path)
            if file_name == 'product_category_name_translation.csv':
                table_name = 'category_translation'
            else:
                table_name = file_name.replace('olist_', '').replace('_dataset.csv', '')

            
            df = pd.read_csv(file_path)

    
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            loaded_tables.append(table_name)
            print(f"✅ Loaded {file_name} → Table '{table_name}' with {len(df)} rows.")

        except Exception as e:
            print(f"⚠️ Error loading {file_name}: {e}")
            return None

    print(f"\n✅ Successfully created database '{db_name}' with tables: {', '.join(loaded_tables)}.")
    return db_path


if __name__ == '__main__':
    print("\n--- DATABASE SETUP START ---")
    print(f"1. Ensure all 9 Olist CSV files are in the '{DATA_DIR}' folder.")
    print(f"2. Running this script will create or overwrite the '{DB_NAME}' file.\n")

    try:
        db_file = load_data_to_db()
        if db_file:
            print(f"\n✅ Database successfully built at: {db_file}")

        
            engine = create_engine(f'sqlite:///{db_file}')
            with engine.connect() as connection:
                result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
                table_names = [row[0] for row in result.fetchall()]

            print("\n📋 Database Schema Tables:")
            for t in table_names:
                print(f"  - {t}")

    except FileNotFoundError as e:
        print(f"\n❌ FATAL ERROR: {e}")
    except Exception as e:
        print(f"\n❌ FATAL ERROR during database creation: {e}")

    print("\n--- DATABASE SETUP END ---")
