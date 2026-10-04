import requests

class GeocodingService:

    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/reverse"

    def reverse_geocode(
        self,
        latitude: float,
        longitude: float
    ) -> dict | None:

        params = {
            "lat": latitude,
            "lon": longitude,
            "format": "jsonv2",
            "addressdetails": 1,
            "zoom": 10,
        }

        headers = {
            "User-Agent": "code-wheater/1.0"
        }

        try:
            response = requests.get(
                self.base_url,
                params=params,
                headers=headers,
                timeout=10,
            )

            response.raise_for_status()

            data = response.json()

            address = data.get("address", {})

            municipality_name = (
                address.get("city")
                or address.get("town")
                or address.get("municipality")
                or address.get("village")
            )

            state = address.get("ISO3166-2-lvl4")

            if state:
                state = state.replace("BR-", "")

            if not municipality_name:
                print(
                    "[GEOCODING] "
                    "Municipality not found."
                )

                return None

            return {
                "name": municipality_name,
                "state": state,
                "latitude": latitude,
                "longitude": longitude,
            }

        except requests.RequestException as error:
            print(
                f"[GEOCODING ERROR] {error}"
            )
            return None

        except ValueError as error:
            print(
                f"[GEOCODING PARSE ERROR] {error}"
            )
            return None