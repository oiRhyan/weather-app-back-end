from langchain_core.tools import tool
from app.repositories.inmet_repository import InmetRepository

inmet_repository = InmetRepository()

@tool
def get_inmet_station(
    station_id: str
) -> dict | None:
    """
    Retorna informações de uma estação meteorológica
    específica do INMET.

    Args:
        station_id: Código da estação.

    Returns:
        Informações da estação ou None.
    """
    print("Calling GET_INMET_STATION summary")
    return inmet_repository.get_station(
        station_id
    )


@tool
def get_inmet_stations() -> list[dict]:
    """
    Retorna todas as estações meteorológicas disponíveis
    no banco de dados do INMET.

    Returns:
        Lista de estações.
    """
    print("Calling GET_INMET_STATIONS summary")
    return inmet_repository.get_all_stations()


@tool
def get_inmet_stations_by_state(
    state: str
) -> list[dict]:
    """
    Retorna as estações meteorológicas do INMET
    localizadas em determinado estado.

    Args:
        state: Sigla do estado. Exemplo: MG, SP, RJ.

    Returns:
        Lista de estações.
    """
    print("Calling GET_INMET_STATIONS_BY_STATE summary")
    return inmet_repository.get_stations_by_state(
        state.upper()
    )


@tool
def get_inmet_observations(
    station_id: str,
    start_date: str,
    end_date: str
) -> list[dict]:
    """
    Retorna as observações meteorológicas de uma estação
    dentro de determinado período.

    Args:
        station_id: Código da estação.
        start_date: Data inicial no formato YYYY-MM-DD.
        end_date: Data final no formato YYYY-MM-DD.

    Returns:
        Lista de observações meteorológicas.
    """
    print("Calling GET_INMET_OBSERVATIONS summary")
    return inmet_repository.get_observations(
        station_id=station_id,
        start_date=start_date,
        end_date=end_date
    )


@tool
def get_inmet_observations_by_date(
    station_id: str,
    date: str
) -> list[dict]:
    """
    Retorna todas as observações meteorológicas de uma
    estação em uma determinada data.

    Args:
        station_id: Código da estação.
        date: Data no formato YYYY-MM-DD.

    Returns:
        Observações horárias da estação.
    """
    print("Calling GET_INMET_OBSERVATIONS_BY_DATE summary")
    return inmet_repository.get_observations_by_date(
        station_id=station_id,
        date=date
    )


@tool
def get_inmet_precipitation(
    station_id: str,
    start_date: str,
    end_date: str
) -> list[dict]:
    """
    Retorna os registros de precipitação de uma estação
    dentro de determinado período.

    Args:
        station_id: Código da estação.
        start_date: Data inicial no formato YYYY-MM-DD.
        end_date: Data final no formato YYYY-MM-DD.

    Returns:
        Registros de precipitação por data e horário.
    """
    print("Calling GET_INMET_PRECIPITATION summary")
    return inmet_repository.get_precipitation(
        station_id=station_id,
        start_date=start_date,
        end_date=end_date
    )


@tool
def get_inmet_weather_summary(
    station_id: str,
    start_date: str,
    end_date: str
) -> dict:
    """
    Retorna um resumo meteorológico de uma estação
    para determinado período.

    O resumo inclui temperatura média, máxima e mínima,
    umidade média, precipitação total e máxima horária,
    velocidade média do vento e rajada máxima.

    Args:
        station_id: Código da estação.
        start_date: Data inicial no formato YYYY-MM-DD.
        end_date: Data final no formato YYYY-MM-DD.

    Returns:
        Resumo meteorológico.
    """
    print("Calling GET_INMET_WEATHER_SUMMARY summary")
    return inmet_repository.get_weather_summary(
        station_id=station_id,
        start_date=start_date,
        end_date=end_date
    )

@tool
def get_nearest_inmet_station(
    latitude: float,
    longitude: float
) -> dict | None:
    """
    Encontra a estação meteorológica do INMET
    mais próxima das coordenadas informadas.

    Args:
        latitude: Latitude da localização.
        longitude: Longitude da localização.

    Returns:
        Dados da estação mais próxima e sua distância
        aproximada em quilômetros.
    """

    print(
        "Calling GET_NEAREST_INMET_STATION summary"
    )

    return inmet_repository.get_nearest_station(
        latitude,
        longitude
    )