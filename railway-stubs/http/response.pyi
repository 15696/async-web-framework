from .abc import Hooker as Hooker
from .hooker import TCPHooker as TCPHooker
from railway.response import HTTPStatus as HTTPStatus
from typing import Any, Dict, Optional, Union

class HTTPResponse:
    status: HTTPStatus = ...
    version: str = ...
    headers: Dict[str, Any] = ...
    def __init__(self, hooker: Union[TCPHooker, Hooker], status: HTTPStatus, version: str, headers: Dict[str, Any], *, body: Optional[bytes]=...) -> None: ...
    def read(self) -> bytes: ...
    def text(self) -> str: ...
    def json(self) -> Dict[str, Any]: ...
