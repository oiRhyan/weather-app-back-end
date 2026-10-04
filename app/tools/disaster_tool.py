from langchain_core.tools import tool
from app.repositories.disaster_repository import DisasterRepository

disaster_repository = DisasterRepository()

@tool
def get_disaster_type_counts(
    ibge_code: int
) -> list[dict]:
    """
    Retorna a quantidade de ocorrências agrupadas
    por tipo de desastre para um município.

    Args:
        ibge_code: Código IBGE do município.

    Returns:
        Lista contendo os tipos de desastre e suas quantidades.
    """
    print("Calling GET_DISASTER_TYPE_COUNTS summary")
    return disaster_repository.get_type_counts(
        ibge_code
    )


@tool
def get_human_damage_summary(
    ibge_code: int
) -> dict:
    """
    Retorna o resumo dos danos humanos causados pelos
    desastres registrados em um município.

    Inclui mortos, feridos, enfermos, desabrigados,
    desalojados, desaparecidos e demais afetados.

    Args:
        ibge_code: Código IBGE do município.

    Returns:
        Resumo dos danos humanos.
    """
    print("Calling GET_HUMAN_DAMAGE_SUMMARY summary")
    return disaster_repository.get_human_damage_summary(
        ibge_code
    )


@tool
def get_material_damage_summary(
    ibge_code: int
) -> dict:
    """
    Retorna o resumo dos danos materiais causados pelos
    desastres registrados em um município.

    Inclui imóveis danificados, imóveis destruídos,
    valor dos danos habitacionais e dano material total.

    Args:
        ibge_code: Código IBGE do município.

    Returns:
        Resumo dos danos materiais.
    """
    print("Calling GET_MATERIAL_DAMAGE_SUMMARY summary")
    return disaster_repository.get_material_damage_summary(
        ibge_code
    )


@tool
def get_disaster_summary(
    ibge_code: int
) -> dict:
    """
    Retorna um resumo completo do histórico de desastres
    de um município.

    Inclui tipos de desastre, danos humanos e danos materiais.

    Args:
        ibge_code: Código IBGE do município.

    Returns:
        Resumo completo dos desastres.
    """
    print("Calling GET_DISASTER_SUMMARY summary")
    return disaster_repository.get_summary(
        ibge_code
    )