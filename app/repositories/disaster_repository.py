import sqlite3
from pathlib import Path
from typing import Any

DATABASE_PATH = Path("data/database/atlas.db")

class DisasterRepository:

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

    def get_type_counts(
        self,
        ibge_code: int
    ) -> list[dict[str, Any]]:

        connection = self._connect()

        try:
            cursor = connection.execute(
                """
                SELECT
                    grupo_de_desastre,
                    COUNT(*) AS total
                FROM disasters
                WHERE Cod_IBGE_Mun = ?
                GROUP BY grupo_de_desastre
                ORDER BY total DESC
                """,
                (ibge_code,)
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:
            connection.close()

    def get_human_damage_summary(
        self,
        ibge_code: int
    ) -> dict[str, Any]:

        connection = self._connect()

        try:
            cursor = connection.execute(
                """
                SELECT

                    COUNT(*) AS total_events,

                    COALESCE(
                        SUM(DH_MORTOS),
                        0
                    ) AS total_deaths,

                    COALESCE(
                        SUM(DH_FERIDOS),
                        0
                    ) AS total_injured,

                    COALESCE(
                        SUM(DH_ENFERMOS),
                        0
                    ) AS total_sick,

                    COALESCE(
                        SUM(DH_DESABRIGADOS),
                        0
                    ) AS total_homeless,

                    COALESCE(
                        SUM(DH_DESALOJADOS),
                        0
                    ) AS total_displaced,

                    COALESCE(
                        SUM(DH_DESAPARECIDOS),
                        0
                    ) AS total_missing,

                    COALESCE(
                        SUM(DH_AFETADOS_SECA_ESTIAGEM),
                        0
                    ) AS drought_affected,

                    COALESCE(
                        SUM(DH_total_danos_humanos_diretos),
                        0
                    ) AS total_direct_human_damage,

                    COALESCE(
                        SUM("DH_OUTROS AFETADOS"),
                        0
                    ) AS total_other_affected

                FROM disasters

                WHERE Cod_IBGE_Mun = ?
                """,
                (ibge_code,)
            )

            row = cursor.fetchone()

            return dict(row) if row else {}

        finally:
            connection.close()

    def get_material_damage_summary(
        self,
        ibge_code: int
    ) -> dict[str, Any]:

        connection = self._connect()

        try:
            cursor = connection.execute(
                """
                SELECT

                    COALESCE(
                        SUM("DM_Uni Habita Danificadas"),
                        0
                    ) AS damaged_houses,

                    COALESCE(
                        SUM("DM_Uni Habita Destruidas"),
                        0
                    ) AS destroyed_houses,

                    COALESCE(
                        SUM("DM_Uni Habita Valor"),
                        0
                    ) AS housing_damage_value,

                    COALESCE(
                        SUM("DM_total_danos_materiais"),
                        0
                    ) AS total_material_damage

                FROM disasters

                WHERE Cod_IBGE_Mun = ?
                """,
                (ibge_code,)
            )

            row = cursor.fetchone()

            return dict(row) if row else {}

        finally:
            connection.close()

    def get_summary(
        self,
        ibge_code: int
    ) -> dict[str, Any]:

        return {
            "human_damage": (
                self.get_human_damage_summary(
                    ibge_code
                )
            ),
            "material_damage": (
                self.get_material_damage_summary(
                    ibge_code
                )
            ),
            "disaster_types": (
                self.get_type_counts(
                    ibge_code
                )
            )
        }