from langchain_core.tools import tool
from app.services.risk_service import RiskService

risk_service = RiskService()

@tool
def calculate_risk(ibge_code: int) -> dict:
    """
    Calcula o nível de risco histórico de um município
    utilizando os dados do Atlas Digital de Desastres.

    Args:
        ibge_code: Código IBGE do município.

    Returns:
        Score, classificação e fatores de risco.
    """

    return risk_service.calculate_risk(
        ibge_code=ibge_code
    )