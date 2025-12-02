from typing import Optional, Type, TypeVar

import requests
from pydantic import TypeAdapter

T = TypeVar("T")


class BaseApiClient:
    def __init__(self, base_url: str, token: str, default_headers: dict = None):
        self.session = requests.Session()
        self.base_url = base_url.rstrip("/")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        if default_headers:
            merged_headers = {**headers, **default_headers}
            self.session.headers.update(merged_headers)
        else:
            self.session.headers.update(headers)

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}/{path.lstrip('/')}"
        return self.session.request(method, url, **kwargs)

    def request_json(self, method: str, path: str, response_model: Optional[Type[T]] = None, **kwargs) -> T:
        resp = self.request(method, path, **kwargs)
        resp.raise_for_status()
        if response_model is None:
            return None
        data = resp.json()
        return TypeAdapter(response_model).validate_python(data)
