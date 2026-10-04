from app.api.DTO.app_response import build_app_response
from app.services.municipiality_service import MunicipalityService
from app.services.inmet_service import InmetService
from app.services.insight_service import InsightService
from app.services.report_service import ReportService
from app.tools.disaster_tool import get_disaster_summary
from app.tools.risk_tool import calculate_risk
from app.tools.wather_tool import get_weather

class WeatherRelatorAgent:

    def __init__(self):
        self.municipality_service = MunicipalityService()
        self.inmet_service = InmetService()
        self.insight_service = InsightService()
        self.report_service = ReportService()

    def run(
        self,
        latitude: float,
        longitude: float,
        forecast_days: int = 7
    ) -> dict:

        weather = get_weather.invoke({
            "latitude": latitude,
            "longitude": longitude,
            "forecast_days": forecast_days
        })

        if not weather:
            return {
                "error": "Unable to retrieve weather data."
            }

        municipality = (
            self.municipality_service.identify_municipality(
                latitude=latitude,
                longitude=longitude
            )
        )

        if not municipality:
            return {
                "error": "Municipality could not be identified."
            }

        ibge_code = municipality["ibge_code"]

        disaster_summary = get_disaster_summary.invoke({
            "ibge_code": ibge_code
        }) or {}

        risk = calculate_risk.invoke({
            "ibge_code": ibge_code
        }) or {}

        inmet = self.inmet_service.get_data(
            latitude=latitude,
            longitude=longitude
        )

        app_data = build_app_response({
            "municipality": municipality,
            "weather": weather,
            "disaster_summary": disaster_summary,
            "risk": risk
        })

        app_data["inmet"] = inmet

        insights = self.insight_service.generate(
            app_data
        )

        report = self.report_service.generate(
            app_data
        )

        return {
            "data": app_data,
            "insights": insights,
            "report": report
        }