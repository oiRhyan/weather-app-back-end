import re
import sqlite3
from pathlib import Path
import pandas as pd

INPUT_DIR = Path("data/raw/inmet")
DATABASE_DIR = Path("data/database")
DATABASE_PATH = DATABASE_DIR / "inmet.db"
CHUNK_SIZE = 50_000

def create_database():
    """
    Cria um novo banco SQLite para os dados do INMET.
    """

    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    # Remove o banco anterior para garantir um schema limpo
    if DATABASE_PATH.exists():
        print("Removendo banco INMET anterior...")
        DATABASE_PATH.unlink()

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE stations (
            station_id TEXT PRIMARY KEY,
            station_name TEXT,
            state TEXT,
            region TEXT,
            latitude REAL,
            longitude REAL,
            altitude REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            station_id TEXT NOT NULL,

            date TEXT,
            hour_utc TEXT,

            precipitation REAL,

            pressure REAL,
            pressure_max REAL,
            pressure_min REAL,

            radiation REAL,

            temperature REAL,
            dew_point REAL,

            temperature_max REAL,
            temperature_min REAL,

            dew_point_max REAL,
            dew_point_min REAL,

            humidity_max REAL,
            humidity_min REAL,
            humidity REAL,

            wind_direction REAL,
            wind_gust REAL,
            wind_speed REAL,

            FOREIGN KEY (station_id)
                REFERENCES stations(station_id)
        )
    """)

    cursor.execute("""
        CREATE INDEX idx_observations_station
        ON observations(station_id)
    """)

    cursor.execute("""
        CREATE INDEX idx_observations_date
        ON observations(date)
    """)

    cursor.execute("""
        CREATE INDEX idx_observations_station_date
        ON observations(station_id, date)
    """)

    connection.commit()

    return connection

def read_file_lines(file_path):
    """
    Lê o arquivo como texto para localizar os metadados
    e o cabeçalho.
    """

    with open(
        file_path,
        "r",
        encoding="latin1",
        errors="replace"
    ) as file:

        return file.readlines()

def find_header(lines):
    """
    Procura a linha real do cabeçalho do INMET.

    Exemplo:

    Data;Hora UTC;PRECIPITAÇÃO TOTAL, HORÁRIO (mm);...
    """

    for index, line in enumerate(lines):

        columns = [
            column.strip()
            .replace("\ufeff", "")
            .lower()
            for column in line.split(";")
        ]

        if len(columns) >= 18:

            if (
                columns[0] == "data"
                and columns[1] == "hora utc"
            ):
                return index

    return None

def normalize_key(key):
    """
    Normaliza a chave dos metadados.
    """

    return (
        key
        .strip()
        .replace("\ufeff", "")
        .upper()
    )


def normalize_decimal(value):
    """
    Converte números no formato brasileiro para float.

    Exemplos:

    1160,96 -> 1160.96
    887,7   -> 887.7
    """

    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    value = value.replace(",", ".")

    try:
        return float(value)

    except (ValueError, TypeError):
        return None


def extract_metadata(lines):
    """
    Extrai os metadados diretamente do arquivo INMET.

    Exemplo:

    REGIAO:;CO
    UF:;DF
    ESTACAO:;BRASILIA
    CODIGO (WMO):;A001
    LATITUDE:;-15,78944444
    LONGITUDE:;-47,92583332
    ALTITUDE:;1160,96
    """

    metadata = {}

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if ";" not in line:
            continue

        key, value = line.split(";", 1)

        key = normalize_key(
            key.replace(":", "")
        )

        value = value.strip()

        metadata[key] = value

    return {
        "station_id": metadata.get("CODIGO (WMO)"),
        "station_name": metadata.get("ESTACAO"),
        "state": metadata.get("UF"),
        "region": metadata.get("REGIAO"),
        "latitude": normalize_decimal(
            metadata.get("LATITUDE")
        ),
        "longitude": normalize_decimal(
            metadata.get("LONGITUDE")
        ),
        "altitude": normalize_decimal(
            metadata.get("ALTITUDE")
        )
    }

def normalize_column_name(column):
    """
    Normaliza nomes das colunas do INMET.
    """

    column = str(column)

    column = (
        column
        .replace("\ufeff", "")
        .strip()
        .upper()
    )

    column = re.sub(
        r"\s+",
        " ",
        column
    )

    return column


def build_column_map(columns):
    """
    Mapeia os nomes reais das colunas do INMET
    para nomes internos simplificados.
    """

    normalized = {
        normalize_column_name(column): column
        for column in columns
    }

    mapping = {}

    def find_column(*patterns):
        """
        Procura uma coluna contendo todos os padrões.
        """

        for normalized_name, original_name in normalized.items():

            if all(
                pattern in normalized_name
                for pattern in patterns
            ):
                return original_name

        return None

    mapping["date"] = find_column(
        "DATA"
    )

    mapping["hour_utc"] = find_column(
        "HORA UTC"
    )

    mapping["precipitation"] = find_column(
        "PRECIPITAÇÃO TOTAL",
        "HORÁRIO"
    )

    mapping["pressure"] = find_column(
        "PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO"
    )

    mapping["pressure_max"] = find_column(
        "PRESSÃO ATMOSFERICA MAX"
    )

    mapping["pressure_min"] = find_column(
        "PRESSÃO ATMOSFERICA MIN"
    )

    mapping["radiation"] = find_column(
        "RADIACAO GLOBAL"
    )

    mapping["temperature"] = find_column(
        "TEMPERATURA DO AR",
        "BULBO SECO"
    )

    mapping["dew_point"] = find_column(
        "TEMPERATURA DO PONTO DE ORVALHO"
    )

    mapping["temperature_max"] = find_column(
        "TEMPERATURA MÁXIMA"
    )

    mapping["temperature_min"] = find_column(
        "TEMPERATURA MÍNIMA"
    )

    mapping["dew_point_max"] = find_column(
        "TEMPERATURA ORVALHO MAX"
    )

    mapping["dew_point_min"] = find_column(
        "TEMPERATURA ORVALHO MIN"
    )

    mapping["humidity_max"] = find_column(
        "UMIDADE REL. MAX"
    )

    mapping["humidity_min"] = find_column(
        "UMIDADE REL. MIN"
    )

    mapping["humidity"] = find_column(
        "UMIDADE RELATIVA DO AR"
    )

    mapping["wind_direction"] = find_column(
        "VENTO, DIREÇÃO HORARIA"
    )

    mapping["wind_gust"] = find_column(
        "VENTO, RAJADA MAXIMA"
    )

    mapping["wind_speed"] = find_column(
        "VENTO, VELOCIDADE HORARIA"
    )

    return mapping

NUMERIC_COLUMNS = [
    "precipitation",
    "pressure",
    "pressure_max",
    "pressure_min",
    "radiation",
    "temperature",
    "dew_point",
    "temperature_max",
    "temperature_min",
    "dew_point_max",
    "dew_point_min",
    "humidity_max",
    "humidity_min",
    "humidity",
    "wind_direction",
    "wind_gust",
    "wind_speed"
]


def convert_numeric(value):
    """
    Converte valores meteorológicos do INMET.

    Exemplos:

    887,7 -> 887.7
    4,5   -> 4.5
    ,8    -> 0.8
    vazio -> None
    """

    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    value = value.replace(",", ".")

    try:
        return float(value)

    except (ValueError, TypeError):
        return None


# ============================================================
# PREPARAÇÃO DO CHUNK
# ============================================================

def normalize_chunk(df, column_map, station_id):
    """
    Converte um chunk do pandas para o formato
    da tabela observations.
    """

    # IMPORTANTE:
    # O DataFrame é criado com o mesmo índice do chunk.
    #
    # Isso garante que:
    #
    # result["station_id"] = station_id
    #
    # seja aplicado a TODAS as linhas.
    result = pd.DataFrame(index=df.index)

    # --------------------------------------------------------
    # Estação
    # --------------------------------------------------------

    result["station_id"] = station_id

    # --------------------------------------------------------
    # Data
    # --------------------------------------------------------

    original = column_map.get("date")

    if original and original in df.columns:

        result["date"] = (
            df[original]
            .astype(str)
            .str.strip()
        )

    else:

        result["date"] = None

    # --------------------------------------------------------
    # Hora UTC
    # --------------------------------------------------------

    original = column_map.get("hour_utc")

    if original and original in df.columns:

        result["hour_utc"] = (
            df[original]
            .astype(str)
            .str.strip()
        )

    else:

        result["hour_utc"] = None

    # --------------------------------------------------------
    # Campos meteorológicos
    # --------------------------------------------------------

    for target_column in NUMERIC_COLUMNS:

        original_column = column_map.get(
            target_column
        )

        if (
            original_column
            and original_column in df.columns
        ):

            result[target_column] = (
                df[original_column]
                .apply(convert_numeric)
            )

        else:

            result[target_column] = None

    return result


# ============================================================
# INSERÇÃO DA ESTAÇÃO
# ============================================================

def insert_station(connection, metadata):
    """
    Insere ou atualiza uma estação.
    """

    connection.execute(
        """
        INSERT OR REPLACE INTO stations (
            station_id,
            station_name,
            state,
            region,
            latitude,
            longitude,
            altitude
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            metadata["station_id"],
            metadata["station_name"],
            metadata["state"],
            metadata["region"],
            metadata["latitude"],
            metadata["longitude"],
            metadata["altitude"]
        )
    )

    connection.commit()


# ============================================================
# INSERÇÃO DAS OBSERVAÇÕES
# ============================================================

def insert_observations(connection, df):
    """
    Insere as observações meteorológicas no SQLite.
    """

    columns = [
        "station_id",
        "date",
        "hour_utc",
        "precipitation",
        "pressure",
        "pressure_max",
        "pressure_min",
        "radiation",
        "temperature",
        "dew_point",
        "temperature_max",
        "temperature_min",
        "dew_point_max",
        "dew_point_min",
        "humidity_max",
        "humidity_min",
        "humidity",
        "wind_direction",
        "wind_gust",
        "wind_speed"
    ]

    placeholders = ", ".join(
        ["?"] * len(columns)
    )

    query = f"""
        INSERT INTO observations (
            {", ".join(columns)}
        )
        VALUES ({placeholders})
    """

    values = [
        tuple(row)
        for row in df[columns].itertuples(
            index=False,
            name=None
        )
    ]

    connection.executemany(
        query,
        values
    )

    connection.commit()


# ============================================================
# PROCESSAMENTO DE UM ARQUIVO
# ============================================================

def process_file(file_path, connection):
    """
    Processa um arquivo CSV do INMET.
    """

    print()
    print("=" * 70)
    print(f"Arquivo: {file_path.name}")

    # --------------------------------------------------------
    # Lê linhas iniciais
    # --------------------------------------------------------

    try:

        lines = read_file_lines(
            file_path
        )

    except Exception as error:

        print(
            f"❌ Erro lendo arquivo: {error}"
        )

        return 0

    # --------------------------------------------------------
    # Metadados
    # --------------------------------------------------------

    metadata = extract_metadata(
        lines
    )

    station_id = metadata["station_id"]

    if not station_id:

        print(
            "⚠ Código WMO não encontrado."
        )

        return 0

    print(
        f"Estação: "
        f"{station_id} | "
        f"{metadata['station_name']} | "
        f"{metadata['state']}"
    )

    # --------------------------------------------------------
    # Cabeçalho
    # --------------------------------------------------------

    header_row = find_header(
        lines
    )

    if header_row is None:

        print(
            "⚠ Cabeçalho não encontrado."
        )

        return 0

    print(
        f"Cabeçalho encontrado na linha "
        f"{header_row + 1}"
    )

    # --------------------------------------------------------
    # Insere estação
    # --------------------------------------------------------

    insert_station(
        connection,
        metadata
    )

    # --------------------------------------------------------
    # Descobre colunas
    # --------------------------------------------------------

    header_line = lines[header_row]

    raw_columns = [
        column.strip()
        for column in header_line.split(";")
    ]

    column_map = build_column_map(
        raw_columns
    )

    # --------------------------------------------------------
    # Validação das colunas obrigatórias
    # --------------------------------------------------------

    missing_required = []

    if not column_map.get("date"):
        missing_required.append("Data")

    if not column_map.get("hour_utc"):
        missing_required.append(
            "Hora UTC"
        )

    if missing_required:

        print(
            "⚠ Colunas obrigatórias não "
            "encontradas:",
            missing_required
        )

        return 0

    # --------------------------------------------------------
    # Leitura em chunks
    # --------------------------------------------------------

    total_records = 0

    try:

        reader = pd.read_csv(
            file_path,
            sep=";",
            encoding="latin1",
            skiprows=header_row,
            dtype=str,
            chunksize=CHUNK_SIZE,
            engine="python"
        )

        for chunk_number, chunk in enumerate(
            reader,
            start=1
        ):

            # Remove possíveis colunas vazias
            # existentes no final do CSV.
            chunk = chunk.drop(
                columns=[
                    column
                    for column in chunk.columns
                    if str(column).strip() == ""
                ],
                errors="ignore"
            )

            normalized = normalize_chunk(
                chunk,
                column_map,
                station_id
            )

            if normalized.empty:
                continue

            insert_observations(
                connection,
                normalized
            )

            records = len(normalized)

            total_records += records

            print(
                f"  Chunk {chunk_number}: "
                f"{records:,} registros"
            )

    except Exception as error:

        print(
            f"❌ Erro processando dados: "
            f"{error}"
        )

        return total_records

    print(
        f"✓ {total_records:,} registros "
        f"importados"
    )

    return total_records


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("INMET IMPORTER")
    print("=" * 70)

    # --------------------------------------------------------
    # Verifica diretório
    # --------------------------------------------------------

    if not INPUT_DIR.exists():

        print(
            f"❌ Diretório não encontrado: "
            f"{INPUT_DIR}"
        )

        return

    # --------------------------------------------------------
    # Busca arquivos
    # --------------------------------------------------------

    files = sorted(
        [
            file
            for file in INPUT_DIR.iterdir()
            if file.is_file()
            and file.suffix.lower() == ".csv"
        ]
    )

    if not files:

        print(
            f"❌ Nenhum CSV encontrado em "
            f"{INPUT_DIR}"
        )

        return

    print(
        f"Arquivos encontrados: "
        f"{len(files)}"
    )

    # --------------------------------------------------------
    # Cria banco
    # --------------------------------------------------------

    connection = create_database()

    processed_files = 0
    empty_files = 0
    total_records = 0

    # --------------------------------------------------------
    # Processa arquivos
    # --------------------------------------------------------

    try:

        for index, file_path in enumerate(
            files,
            start=1
        ):

            print()
            print(
                f"[{index}/{len(files)}] "
                f"Processando: "
                f"{file_path.name}"
            )

            records = process_file(
                file_path,
                connection
            )

            if records > 0:

                processed_files += 1
                total_records += records

            else:

                empty_files += 1

    finally:

        connection.close()

    # --------------------------------------------------------
    # Resultado
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("INMET IMPORTADO!")
    print("=" * 70)

    print(
        f"Arquivos encontrados: "
        f"{len(files)}"
    )

    print(
        f"Arquivos processados: "
        f"{processed_files}"
    )

    print(
        f"Arquivos sem registros: "
        f"{empty_files}"
    )

    print(
        f"Registros: "
        f"{total_records:,}"
    )

    print(
        f"Banco: "
        f"{DATABASE_PATH}"
    )

    print("=" * 70)

if __name__ == "__main__":
    main()