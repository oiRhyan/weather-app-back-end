from langchain_core.tools import tool
from app.repositories.atlas_repository import AtlasRepository

atlas_repository = AtlasRepository()

@tool
def get_disasters_by_municipality(
    ibge_code: int
) -> list[dict]:
    """
    Retorna o histórico completo de desastres registrados
    para um município no Atlas Digital de Desastres.

    Args:
        ibge_code: Código IBGE do município.

    Returns:
        Lista de registros de desastres.
    """
    print("Calling GET_DISASTER_BY_MUNICIPIO summary")
    return atlas_repository.get_by_municipality(
        ibge_code
    )


@tool
def get_disasters_by_period(
    ibge_code: int,
    start_date: str,
    end_date: str
) -> list[dict]:
    """
    Retorna os desastres registrados para um município
    dentro de um determinado período.

    Args:
        ibge_code: Código IBGE do município.
        start_date: Data inicial no formato YYYY-MM-DD.
        end_date: Data final no formato YYYY-MM-DD.

    Returns:
        Lista de desastres registrados no período.
    """
    print("Calling GET_DISASTER_BY_PERIODO summary")
    return atlas_repository.get_by_period(
        ibge_code=ibge_code,
        start_date=start_date,
        end_date=end_date
    )


@tool
def get_disaster_by_protocol(
    protocol: str
) -> dict | None:
    """
    Retorna um desastre específico através do protocolo S2iD.

    Args:
        protocol: Número do protocolo S2iD.

    Returns:
        Registro do desastre ou None caso não seja encontrado.
    """
    print("Calling GET_DISASTER_BY_PROTOCOLO summary")
    return atlas_repository.get_by_protocol(
        protocol
    )


@tool
def get_municipalities() -> list[dict]:
    """
    Retorna os municípios disponíveis no Atlas Digital
    de Desastres, incluindo código IBGE, nome, estado e região.

    Returns:
        Lista de municípios.
    """
    print("Calling GET_MUNICIPIOS summary")
    return atlas_repository.get_municipalities()