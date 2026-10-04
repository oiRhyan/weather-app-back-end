from typing import Any

def _safe_max(values: list[Any]) -> float | None:
    values = [value for value in values if value is not None]

    if not values:
        return None

    return max(values)


def _safe_min(values: list[Any]) -> float | None:
    values = [value for value in values if value is not None]

    if not values:
        return None

    return min(values)


def build_app_response(data: dict) -> dict:
    municipality = data.get("municipality") or {}
    weather = data.get("weather") or {}
    disaster = data.get("disaster_summary") or {}
    risk = data.get("risk") or {}
    current = weather.get("current") or {}
    daily = weather.get("daily") or {}

    dates = daily.get("time") or []

    temperature_max = (
        daily.get("temperature_2m_max") or []
    )

    temperature_min = (
        daily.get("temperature_2m_min") or []
    )

    precipitation = (
        daily.get("precipitation_sum") or []
    )

    precipitation_probability = (
        daily.get(
            "precipitation_probability_max"
        ) or []
    )

    wind_max = (
        daily.get("wind_speed_10m_max") or []
    )

    forecast_days = []

    for index, forecast_date in enumerate(dates):

        forecast_days.append(
            {
                "date": forecast_date,

                "temperature_max": (
                    temperature_max[index]
                    if index < len(temperature_max)
                    else None
                ),

                "temperature_min": (
                    temperature_min[index]
                    if index < len(temperature_min)
                    else None
                ),

                "precipitation_mm": (
                    precipitation[index]
                    if index < len(precipitation)
                    else None
                ),

                "precipitation_probability": (
                    precipitation_probability[index]
                    if index < len(
                        precipitation_probability
                    )
                    else None
                ),

                "wind_max_kmh": (
                    wind_max[index]
                    if index < len(wind_max)
                    else None
                ),
            }
        )

    max_precipitation = _safe_max(
        precipitation
    )

    max_probability = _safe_max(
        precipitation_probability
    )

    highest_precipitation_day = None

    if (
        max_precipitation is not None
        and precipitation
    ):
        try:
            index = precipitation.index(
                max_precipitation
            )

            if index < len(dates):
                highest_precipitation_day = (
                    dates[index]
                )

        except ValueError:
            highest_precipitation_day = None

    human = (
        disaster.get("human_damage") or {}
    )

    material = (
        disaster.get("material_damage") or {}
    )

    disaster_types = (
        disaster.get("disaster_types") or []
    )

    main_disaster_type = None

    if disaster_types:

        main_type = max(
            disaster_types,
            key=lambda item: (
                item.get("total", 0) or 0
            ),
        )

        main_disaster_type = (
            main_type.get(
                "grupo_de_desastre"
            )
        )

    return {

        "location": {
            "municipality": municipality.get(
                "name"
            ),
            "state": municipality.get(
                "state"
            ),
            "ibge_code": municipality.get(
                "ibge_code"
            ),
        },

        "current": {
            "temperature": current.get(
                "temperature_2m"
            ),
            "humidity": current.get(
                "relative_humidity_2m"
            ),
            "precipitation_mm": current.get(
                "precipitation"
            ),
            "wind_speed_kmh": current.get(
                "wind_speed_10m"
            ),
            "wind_gust_kmh": current.get(
                "wind_gusts_10m"
            ),
            "pressure_hpa": current.get(
                "pressure_msl"
            ),
        },

        "forecast": {

            "days": forecast_days,

            "summary": {
                "max_precipitation_mm": (
                    max_precipitation
                ),

                "max_precipitation_probability": (
                    max_probability
                ),

                "highest_precipitation_day": (
                    highest_precipitation_day
                ),

                "temperature_min": _safe_min(
                    temperature_min
                ),

                "temperature_max": _safe_max(
                    temperature_max
                ),

                "wind_max_kmh": _safe_max(
                    wind_max
                ),
            },
        },

        "risk": {
            "score": risk.get(
                "score"
            ),

            "level": risk.get(
                "level"
            ),

            "factors": risk.get(
                "factors",
                []
            ),
        },

        "historical": {

            "total_events": human.get(
                "total_events",
                0
            ),

            "deaths": human.get(
                "total_deaths",
                0
            ),

            "injured": human.get(
                "total_injured",
                0
            ),

            "displaced": human.get(
                "total_displaced",
                0
            ),

            "homeless": human.get(
                "total_homeless",
                0
            ),

            "destroyed_houses": material.get(
                "destroyed_houses",
                0
            ),

            "damaged_houses": material.get(
                "damaged_houses",
                0
            ),

            "total_material_damage": (
                material.get(
                    "total_material_damage",
                    0
                )
            ),

            "main_disaster_type": (
                main_disaster_type
            ),
        },

        "alerts": [],
    }