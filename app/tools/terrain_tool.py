from langchain_core.tools import tool

@tool
def get_terrain(
    latitude: float,
    longitude: float
) -> dict:
    """
    Obtém informações de terreno para uma localização.

    Args:
        latitude: Latitude da localização.
        longitude: Longitude da localização.

    Returns:
        Informações de elevação e terreno.
    """

    raise NotImplementedError(
        "Terrain provider ainda não foi implementado."
    )