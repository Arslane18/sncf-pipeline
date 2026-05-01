import requests
from dagster import ConfigurableResource


class SNCFResource(ConfigurableResource):
    sncf_token: str | None

    def connect(self, api_url: str):
        """Establishes a connection to the SNCF API and returns the response data."""
        resp = requests.get(
            api_url,
            headers={"Authorization": self.sncf_token},
            params={"count": 100}
        )

        resp.raise_for_status()

        return resp.json()