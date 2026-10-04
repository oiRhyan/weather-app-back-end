from app.repositories.disaster_repository import DisasterRepository

class RiskService:

    def __init__(self):
        self.disaster_repository = DisasterRepository()

    def calculate_risk(self, ibge_code: int) -> dict:
        """
        Calcula o risco histórico de desastre de um município
        com base nos dados do Atlas Digital de Desastres.

        Args:
            ibge_code: Código IBGE do município.

        Returns:
            Score, nível de risco, fatores e dados históricos.
        """
        summary = self.disaster_repository.get_summary(
            ibge_code=ibge_code
        )

        human_damage = summary.get("human_damage", {}) or {}
        material_damage = summary.get("material_damage", {}) or {}

        total_occurrences = human_damage.get(
            "total_events",
            0
        ) or 0

        if total_occurrences == 0:
            return {
                "ibge_code": ibge_code,
                "score": 0,
                "level": "UNKNOWN",
                "factors": [
                    "Não foram encontrados registros históricos de desastres."
                ],
                "historical_data": summary
            }

        score = 0
        factors = []

        if total_occurrences >= 20:
            score += 40
            factors.append(
                "Alta frequência histórica de desastres"
            )

        elif total_occurrences >= 10:
            score += 30
            factors.append(
                "Frequência histórica moderada de desastres"
            )

        elif total_occurrences >= 5:
            score += 20
            factors.append(
                "Baixa frequência histórica de desastres"
            )

        else:
            score += 10
            factors.append(
                "Frequência histórica de desastres muito baixa."
            )

        deaths = human_damage.get("deaths", 0) or 0
        injured = human_damage.get("injured", 0) or 0
        homeless = human_damage.get("homeless", 0) or 0
        displaced = human_damage.get("displaced", 0) or 0

        if deaths > 0:
            score += 25
            factors.append(
                f"Mortes históricas: {deaths}"
            )

        if injured > 0:
            score += 10
            factors.append(
                f"Lesões históricas: {injured}"
            )

        if homeless > 0 or displaced > 0:
            score += 10
            factors.append(
                "Deslocamento histórico da população"
            )

        total_material_damage = material_damage.get(
            "total_material_damage",
            0
        ) or 0

        if total_material_damage >= 10_000_000:
            score += 15
            factors.append(
                "Danos materiais históricos muito elevados"
            )

        elif total_material_damage >= 1_000_000:
            score += 10
            factors.append(
                "Grandes danos materiais históricos"
            )

        elif total_material_damage > 0:
            score += 5
            factors.append(
                "Historical material damage recorded"
            )

        score = min(score, 100)

        level = self._classify_risk(score)

        return {
            "ibge_code": ibge_code,
            "score": score,
            "level": level,
            "factors": factors,
            "historical_data": summary
        }

    @staticmethod
    def _classify_risk(score: int) -> str:
        if score >= 70:
            return "Alto"
        if score >= 40:
            return "Médio"
        return "Baixo"