import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()


class Client:
    def __init__(self, client_id: str, client_secret: str):
        self.token_url = os.getenv("TOKEN_URL")
        self.base_url = os.getenv("BASE_URL")
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self._get_access_token()

    def _get_access_token(self) -> str:
        response = requests.post(
            self.token_url,
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            data={"grant_type": "client_credentials"},
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def fetch_data(self, url: str) -> Dict[str, Any]:
        response = requests.get(url, headers=self.get_headers())
        return response.json()
