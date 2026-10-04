from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from app.utils.llm_parser import parse_insights

class InsightService:

    def __init__(self):

        self.llm = ChatOllama(
            model="qwen3:0.6b",
            temperature=0.2
        )

    def generate(
        self,
        app_data: dict
    ) -> dict:

        prompt = self._build_prompt(app_data)

        try:

            response = self.llm.invoke([
                HumanMessage(
                    content=prompt
                )
            ])

            content = response.content.strip()

            print("\n[LLM INSIGHTS RAW]")
            print(content)

            return parse_insights(content)

        except Exception as error:

            print(
                f"[LLM INSIGHTS ERROR] {error}"
            )

            return self._empty_response()

    def _build_prompt(
        self,
        app_data: dict
    ) -> str:

        current = (
            app_data.get("current")
            or {}
        )

        forecast = (
            app_data.get("forecast")
            or {}
        )

        forecast_summary = (
            forecast.get("summary")
            or {}
        )

        risk = (
            app_data.get("risk")
            or {}
        )

        historical = (
            app_data.get("historical")
            or {}
        )

        return f"""
Gere exatamente quatro frases curtas em português.

Use SOMENTE os dados abaixo.

SITUAÇÃO ATUAL:

Temperatura:
{current.get("temperature")} °C

Umidade:
{current.get("humidity")} %

Precipitação atual:
{current.get("precipitation_mm")} mm

Vento:
{current.get("wind_speed_kmh")} km/h


PREVISÃO:

Maior precipitação prevista:
{forecast_summary.get("max_precipitation_mm")} mm

Maior probabilidade de precipitação:
{forecast_summary.get("max_precipitation_probability")} %

Dia da maior precipitação prevista:
{forecast_summary.get("highest_precipitation_day")}


RISCO:

Score:
{risk.get("score")}

Nível:
{risk.get("level")}

Fatores:
{risk.get("factors")}


HISTÓRICO:

Total de eventos:
{historical.get("total_events")}


REGRAS:

- Não invente informações.
- Não invente números.
- Não altere números.
- Não invente alertas.
- Não invente fenômenos meteorológicos.
- Não invente fatores de risco.
- Não diga que uma previsão já aconteceu.
- Não diga que um desastre acontecerá.
- Não transforme probabilidade em certeza.
- Precipitação é medida em mm.
- Temperatura é medida em °C.
- Vento é medido em km/h.
- Use exatamente os fatores de risco fornecidos.
- Seja objetivo.
- Não escreva explicações.
- Não use Markdown.


FORMATO EXATO:

RESUMO: situação meteorológica atual.

CHUVA: previsão de precipitação.

RISCO: score, nível e fatores.

ATENÇÃO: informação meteorológica relevante da previsão.

Substitua cada frase acima pelos dados reais.
"""

    @staticmethod
    def _empty_response() -> dict:

        return {
            "summary": "",
            "precipitation": "",
            "risk": "",
            "danger": ""
        }