import json
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from app.utils.llm_parser import parse_report

class ReportService:

    def __init__(self):

        self.llm = ChatOllama(
            model="qwen3:0.6b",
            temperature=0.2
        )

    def generate(
        self,
        app_data: dict
    ) -> dict:

        prompt_data = self._prepare_data(
            app_data
        )

        prompt = self._build_prompt(
            prompt_data
        )

        try:
            response = self.llm.invoke([
                HumanMessage(
                    content=prompt
                )
            ])

            content = response.content.strip()

            print("\n[LLM REPORT RAW]")
            print(content)

            return parse_report(content)

        except Exception as error:
            print(
                f"[LLM REPORT ERROR] {error}"
            )
            return self._empty_response()

    def _prepare_data(
        self,
        app_data: dict
    ) -> dict:

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

        historical = (
            app_data.get("historical")
            or {}
        )

        inmet = (
            app_data.get("inmet")
            or {}
        )

        risk = (
            app_data.get("risk")
            or {}
        )

        return {
            "current": {
                "temperature":
                    current.get("temperature"),
                "humidity":
                    current.get("humidity"),
                "precipitation_mm":
                    current.get("precipitation_mm"),
                "wind_speed_kmh":
                    current.get("wind_speed_kmh"),
                "wind_gust_kmh":
                    current.get("wind_gust_kmh"),
                "pressure_hpa":
                    current.get("pressure_hpa")
            },
            "forecast": {
                "max_precipitation_mm":
                    forecast_summary.get(
                        "max_precipitation_mm"
                    ),
                "max_precipitation_probability":
                    forecast_summary.get(
                        "max_precipitation_probability"
                    ),
                "highest_precipitation_day":
                    forecast_summary.get(
                        "highest_precipitation_day"
                    ),
                "temperature_min":
                    forecast_summary.get(
                        "temperature_min"
                    ),
                "temperature_max":
                    forecast_summary.get(
                        "temperature_max"
                    ),
                "wind_max_kmh":
                    forecast_summary.get(
                        "wind_max_kmh"
                    )
            },
            "historical": historical,
            "inmet": self._prepare_inmet(
                inmet
            ),
            "risk": risk
        }

    @staticmethod
    def _prepare_inmet(
        inmet: dict
    ) -> dict:

        has_data = inmet.get(
            "has_data",
            False
        )
        return {
            "available": inmet.get(
                "available",
                False
            ),
            "has_data": has_data,
            "station": inmet.get(
                "station"
            ),
            "period": inmet.get(
                "period"
            ),
            "summary": (
                inmet.get("summary")
                if has_data
                else None
            )
        }

    def _build_prompt(
        self,
        data: dict
    ) -> str:
        json_data = json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
            default=str
        )

        return f"""
Você é um analista meteorológico.

Transforme os dados abaixo em um relatório textual.

DADOS:

{json_data}


REGRAS ABSOLUTAS:

1. Use somente os dados fornecidos.

2. Não invente informações.

3. Não invente números.

4. Não altere números.

5. Não estime valores null.

6. Não crie alertas.

7. Não crie fatores de risco.

8. Não diga que um desastre acontecerá.

9. Não transforme previsão em ocorrência.

10. Diferencie claramente condições atuais,
previsão e histórico.

11. Se INMET estiver disponível mas
has_data=false, explique que a estação
foi encontrada, porém não existem
medições agregadas disponíveis para
o período consultado.

12. Se algum dado estiver null,
não invente um valor.

13. Não use conhecimento externo.

14. Não use Markdown.

15. Cada seção deve ser uma única
frase ou pequeno parágrafo.

16. Não repita desnecessariamente
os mesmos números.

17. O score e o nível de risco devem
ser exatamente os fornecidos.

18. Os fatores de risco devem ser
usados exatamente como fornecidos.


Gere exatamente estas seções:

CURRENT:
Descreva as condições meteorológicas atuais.

FORECAST:
Descreva a previsão meteorológica.

PRECIPITATION:
Descreva a precipitação prevista,
sua probabilidade máxima e o dia
de maior precipitação.

HISTORICAL:
Descreva resumidamente o histórico
de desastres.

INMET:
Descreva a situação da estação
e a disponibilidade dos dados.

RISK:
Descreva o score, nível e fatores de risco.

GENERAL:
Faça uma síntese geral sem criar
informações novas.


IMPORTANTE:

Não escreva JSON.
Não escreva listas.
Não escreva explicações fora
das sete seções.

Formato obrigatório:

CURRENT: texto
FORECAST: texto
PRECIPITATION: texto
HISTORICAL: texto
INMET: texto
RISK: texto
GENERAL: texto
"""

    @staticmethod
    def _empty_response() -> dict:

        return {
            "current": "",
            "forecast": "",
            "precipitation": "",
            "historical": "",
            "inmet": "",
            "risk": "",
            "general": ""
        }