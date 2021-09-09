from . import http
from .app import Application
from typing import Any

class TestClient:
    app: Application = ...
    session: http.HTTPSession = ...
    def __init__(self, app: Application) -> None: ...
    @property
    def host(self) -> str: ...
    @property
    def port(self) -> int: ...
    def ws_connect(self, path: str) -> http.AsyncContextManager[http.Websocket]: ...
    def request(self, path: str, method: str, **kwargs: Any) -> http.AsyncContextManager[http.HTTPResponse]: ...
    def get(self, path: str, **kwargs: Any) -> Any: ...
    def post(self, path: str, **kwargs: Any) -> Any: ...
    def put(self, path: str, **kwargs: Any) -> Any: ...
    def delete(self, path: str, **kwargs: Any) -> Any: ...
