import asyncio
from .hooker import TCPHooker, Websocket
from .response import HTTPResponse
from .utils import AsyncContextManager
from typing import Any, Optional

class HTTPSession:
    loop: asyncio.AbstractEventLoop = ...
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop]=...) -> None: ...
    async def __aenter__(self): ...
    async def __aexit__(self, *exc: Any) -> Any: ...
    async def close(self) -> None: ...
    def request(self, method: str, url: str, **kwargs: Any) -> AsyncContextManager[HTTPResponse]: ...
    def ws_connect(self, url: str, **kwargs: Any) -> AsyncContextManager[Optional[Websocket]]: ...
    def get(self, url: str, **kwargs: Any) -> Any: ...
    def post(self, url: str, **kwargs: Any) -> Any: ...
    def put(self, url: str, **kwargs: Any) -> Any: ...
    def delete(self, url: str, **kwargs: Any) -> Any: ...
    def head(self, url: str, **kwargs: Any) -> Any: ...
    async def redirect(self, hooker: TCPHooker, response: HTTPResponse, method: str) -> HTTPResponse: ...

def request(url: str, method: str, **kwargs: Any) -> AsyncContextManager[HTTPResponse]:: ...
def ws_connect(url: str, **kwargs: Any) -> AsyncContextManager[Websocket]: ...