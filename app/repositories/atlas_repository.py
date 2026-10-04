import sqlite3
from pathlib import Path
from typing import Any

DATABASE_PATH = Path("data/database/atlas.db")

class AtlasRepository:

    def __init__(
        self,
        database_path: str | Path = DATABASE_PATH
    ):
        self.database_path = database_path

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.database_path
        )

        connection.row_factory = sqlite3.Row

        return connection

    def get_by_municipality(
        self,
        ibge_code: int
    ) -> list[dict[str, Any]]:

        connection = self._connect()

        try:
            cursor = connection.execute(
                """
                SELECT *
                FROM disasters
                WHERE Cod_IBGE_Mun = ?
                ORDER BY Data_Evento DESC
                """,
                (ibge_code,)
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:
            connection.close()

    def get_by_period(
        self,
        ibge_code: int,
        start_date: str,
        end_date: str
    ) -> list[dict[str, Any]]:

        connection = self._connect()

        try:
            cursor = connection.execute(
                """
                SELECT *
                FROM disasters
                WHERE Cod_IBGE_Mun = ?
                  AND Data_Evento BETWEEN ? AND ?
                ORDER BY Data_Evento DESC
                """,
                (
                    ibge_code,
                    start_date,
                    end_date
                )
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:
            connection.close()

    def get_by_protocol(
        self,
        protocol: str
    ) -> dict[str, Any] | None:

        connection = self._connect()

        try:
            cursor = connection.execute(
                """
                SELECT *
                FROM disasters
                WHERE Protocolo_S2iD = ?
                """,
                (protocol,)
            )

            row = cursor.fetchone()

            return dict(row) if row else None

        finally:
            connection.close()

    def get_municipality(
    self,
    name: str,
    state: str | None = None
    ) -> dict | None:

        connection = self._connect()

        try:
            cursor = connection.cursor()

            if state:
                cursor.execute(
                    """
                    SELECT
                        Cod_IBGE_Mun,
                        Nome_Municipio,
                        Sigla_UF
                    FROM disasters
                    WHERE UPPER(TRIM(Nome_Municipio)) = UPPER(TRIM(?))
                    AND UPPER(TRIM(Sigla_UF)) = UPPER(TRIM(?))
                    LIMIT 1
                    """,
                    (
                        name,
                        state,
                    )
                )

            else:
                cursor.execute(
                    """
                    SELECT
                        Cod_IBGE_Mun,
                        Nome_Municipio,
                        Sigla_UF
                    FROM disasters
                    WHERE UPPER(TRIM(Nome_Municipio)) = UPPER(TRIM(?))
                    LIMIT 1
                    """,
                    (name,)
                )

            row = cursor.fetchone()

            if not row:
                return None

            return {
                "ibge_code": row[0],
                "name": row[1],
                "state": row[2],
            }

        finally:
            connection.close()


    def get_municipality_by_ibge(self, ibge_code: int) -> dict | None:
        connection = self._connect()

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    Cod_IBGE_Mun,
                    Nome_Municipio,
                    Sigla_UF
                FROM disasters
                WHERE Cod_IBGE_Mun = ?
                LIMIT 1
                """,
                (ibge_code,)
            )

            row = cursor.fetchone()

            if not row:
                return None

            return {
                "ibge_code": row[0],
                "name": row[1],
                "state": row[2],
            }
        finally:
            connection.close()