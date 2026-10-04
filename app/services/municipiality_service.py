from app.repositories.atlas_repository import AtlasRepository
from app.services.geocoding_service import GeocodingService

class MunicipalityService:

    def __init__(self):

        self.geocoding_service = (
            GeocodingService()
        )

        self.atlas_repository = (
            AtlasRepository()
        )

    def identify_municipality(
        self,
        latitude: float,
        longitude: float
    ) -> dict | None:

        location = (
            self.geocoding_service
            .reverse_geocode(
                latitude=latitude,
                longitude=longitude,
            )
        )

        if not location:

            return None

        municipality_name = location.get(
            "name"
        )

        state = location.get(
            "state"
        )

        if not municipality_name:

            return None

        print(
            "[GEOCODING]"
            f" {municipality_name}"
            f" - {state}"
        )

        municipality = (
            self.atlas_repository
            .get_municipality(
                name=municipality_name,
                state=state,
            )
        )

        if not municipality:

            print(
                "[MUNICIPALITY]"
                " Municipality not found in Atlas:"
                f" {municipality_name}"
                f" - {state}"
            )

            return None

        print(
            "[MUNICIPALITY]"
            f" {municipality['name']}"
            f" - {municipality['state']}"
            f" - IBGE {municipality['ibge_code']}"
        )

        return {
            "name": municipality["name"],
            "state": municipality["state"],
            "ibge_code": municipality["ibge_code"],
            "latitude": latitude,
            "longitude": longitude,
        }