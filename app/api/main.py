from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.agents.AnaliticAgent import WeatherRelatorAgent

app = FastAPI(
    title="Code Wheater API",
    description="API de análise meteorológica e risco de desastres",
    version="1.0.0"
)

agent = WeatherRelatorAgent()

class WeatherRequest(BaseModel):
    latitude: float = Field(..., description="Latitude da localização")
    longitude: float = Field(..., description="Longitude da localização")
    forecast_days: int = Field(
        default=7,
        ge=1,
        le=16,
        description="Quantidade de dias da previsão"
    )

@app.get("/")
def root():
    return {
        "name": "Code Wheater API",
        "status": "online"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/api/weather/report")
def generate_report(request: WeatherRequest):
    try:
        result = agent.run(
            latitude=request.latitude,
            longitude=request.longitude,
            forecast_days=request.forecast_days
        )

        return result

    except Exception as exception:
        raise HTTPException(
            status_code=500,
            detail=str(exception)
        )