import os
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

from entity import Class, User

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
        response.raise_for_status()
        return response.json()

    def get_all_teachers(
        self, *, params: Optional[Dict[str, Any]] = None
    ) -> List[User]:
        url = f"{self.base_url}/teachers"
        if params:
            url = f"{url}?{urlencode(params)}"

        data = self.fetch_data(url)

        return [User.decode(user_data) for user_data in data["users"]]

    def get_classes_for_teacher(
        self, teacher_sourced_id: str, *, params: Optional[Dict[str, Any]] = None
    ) -> List[Class]:
        url = f"{self.base_url}/teachers/{teacher_sourced_id}/classes"
        if params:
            url = f"{url}?{urlencode(params)}"

        data = self.fetch_data(url)

        return [Class.decode(class_data) for class_data in data["classes"]]

    def get_students_for_class(
        self, class_sourced_id: str, *, params: Optional[Dict[str, Any]] = None
    ) -> List[User]:
        url = f"{self.base_url}/classes/{class_sourced_id}/students"
        if params:
            url = f"{url}?{urlencode(params)}"

        data = self.fetch_data(url)

        return [User.decode(user_data) for user_data in data["users"]]
