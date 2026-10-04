import requests

class ApiClient:

    def __init__(self, base_url: str, timeout: int = 60000):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get(self, endpoint: str, params: dict | None = None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        response = requests.get(
            url,
            params=params,
            timeout=self.timeout
        )

        response.raise_for_status()

        return response.json()