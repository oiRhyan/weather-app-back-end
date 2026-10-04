import sqlite3
import pandas as pd

EXCEL_PATH = "data/raw/atlas/BD_Atlas_1991_2025_v1.1_2026.08.06_Consolidado.xlsx"
DATABASE_PATH = "database/atlas.db"

def main():
    df = pd.read_excel(EXCEL_PATH)

    connection = sqlite3.connect(DATABASE_PATH)

    df.to_sql(
        "disasters",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()

    print(f"Atlas importado: {len(df)} registros")

if __name__ == "__main__":
    main()