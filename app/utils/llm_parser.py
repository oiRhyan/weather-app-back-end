def parse_insights(
    content: str
) -> dict:

    insights = {
        "summary": "",
        "precipitation": "",
        "risk": "",
        "danger": ""
    }

    sections = {
        "RESUMO:": "summary",
        "CHUVA:": "precipitation",
        "RISCO:": "risk",
        "ATENÇÃO:": "danger"
    }

    for line in content.splitlines():

        line = line.strip()

        if not line:
            continue

        upper_line = line.upper()

        for marker, key in sections.items():

            if upper_line.startswith(marker):

                insights[key] = (
                    line.split(
                        ":",
                        1
                    )[1].strip()
                )

                break

    return insights


def parse_report(
    content: str
) -> dict:

    report = {
        "current": "",
        "forecast": "",
        "precipitation": "",
        "historical": "",
        "inmet": "",
        "risk": "",
        "general": ""
    }

    sections = {
        "CURRENT:": "current",
        "FORECAST:": "forecast",
        "PRECIPITATION:": "precipitation",
        "HISTORICAL:": "historical",
        "INMET:": "inmet",
        "RISK:": "risk",
        "GENERAL:": "general"
    }

    current_section = None

    for line in content.splitlines():

        line = line.strip()

        if not line:
            continue

        upper_line = line.upper()

        found_section = None

        for marker, key in sections.items():

            if upper_line.startswith(marker):

                found_section = key

                text = line[
                    len(marker):
                ].strip()

                if text:
                    report[key] = text

                break

        if found_section:

            current_section = found_section

            continue

        if current_section:

            if report[current_section]:

                report[current_section] += (
                    " " + line
                )

            else:

                report[current_section] = line

    return report