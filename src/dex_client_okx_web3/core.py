from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Mapping
from urllib.parse import urljoin

import httpx

try:
    from curl_cffi import requests as curl_requests
except Exception:  # pragma: no cover
    curl_requests = None

Json = dict[str, Any]

DEFAULT_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

class APIError(RuntimeError):
    def __init__(self, message: str, *, status_code: int | None = None, payload: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload

@dataclass(slots=True)
class BaseClient:
    base_url: str
    timeout: float = 10.0
    headers: dict[str, str] = field(default_factory=dict)
    use_curl_cffi: bool = False

    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")
        self._client = httpx.Client(timeout=self.timeout, headers={"User-Agent": DEFAULT_UA, **self.headers})

    def close(self) -> None:
        self._client.close()

    def _url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return self.base_url + "/" + path.lstrip("/")

    def request(self, method: str, path: str, *, params: Mapping[str, Any] | None = None, json_body: Any = None, data: Any = None, headers: Mapping[str, str] | None = None, curl_cffi: bool | None = None) -> Json:
        url = self._url(path)
        merged_headers = {**self.headers, **(headers or {})}
        use_curl = self.use_curl_cffi if curl_cffi is None else curl_cffi
        if use_curl:
            if curl_requests is None:
                raise APIError("curl_cffi is not installed")
            resp = curl_requests.request(method, url, params=params, json=json_body, data=data, headers=merged_headers, timeout=self.timeout, impersonate="chrome124")
            text = resp.text
            status = resp.status_code
        else:
            resp = self._client.request(method, url, params=params, json=json_body, data=data, headers=merged_headers)
            text = resp.text
            status = resp.status_code
        if status < 200 or status >= 300:
            raise APIError(f"{method} {url} failed with HTTP {status}", status_code=status, payload=text[:1000])
        if not text:
            return {}
        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            raise APIError(f"{method} {url} returned non-json", status_code=status, payload=text[:1000]) from exc
        return payload

    def get(self, path: str, **kwargs: Any) -> Json:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Json:
        return self.request("POST", path, **kwargs)

def now_ms() -> int:
    return int(time.time() * 1000)

def drop_empty(values: Mapping[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in values.items() if v is not None and v != ""}
