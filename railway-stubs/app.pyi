from .errors import *
import asyncio
import pathlib
import socket as _socket
import ssl
from ._types import CoroFunc, Coro
from .file import File
from .injectables import Injectable
from .objects import Listener, Middleware, PartialRoute, Route, WebsocketRoute
from .request import Request
from .resources import Resource
from .response import Response
from .router import Router
from .settings import Settings
from .views import HTTPView
from .responses import HTTPException
from .datastructures import URL
from .workers import Worker
from .locks import Semaphore
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union

class Application:
    settings: Settings = ...
    host: str = ...
    port: int = ...
    url_prefix: str = ...
    router: Router = ...
    ssl_context: Optional[ssl.SSLContext] = ...
    worker_count: int = ...
    WILDCARD_METHODS: List[str] = ...
    def __init__(self, 
        host: str=..., 
        port: int=..., 
        url_prefix: str=..., 
        *, 
        loop: asyncio.AbstractEventLoop=..., 
        settings: Settings=...,
        settings_file: Union[str, pathlib.Path]=..., 
        load_settings_from_env: bool=..., 
        ipv6: bool=..., 
        sock: _socket.socket=..., 
        worker_count: int=..., 
        use_ssl: bool=..., 
        ssl_context: ssl.SSLContext=...,                
        max_pending_connections: int=...,
        max_concurent_requests: int=...,
        connection_timeout: int=...,
        backlog: int=...,
        reuse_host: bool=...,
        reuse_port: bool=...
    ) -> None: ...
    async def __aenter__(self) -> Application: ...
    def __getitem__(self, item: str): ...
    def create_ipv6_socket(self, host: str, port: int) -> _socket.socket: ...
    def create_ipv4_socket(self, host: str, port: int) -> _socket.socket: ...
    def create_default_ssl_context(self) -> ssl.SSLContext: ...
    async def parse_response(
        self, 
        response: Union[str, bytes, Dict[str, Any], List[Any], Tuple[Any, Any], File, Response, Any]
    ) -> Optional[Response]: ...
    def set_default_cookie(self, request: Request, response: Response) -> Response: ...
    @property
    def reuse_host(self) -> bool: ...
    @property
    def reuse_port(self) -> bool: ...
    @property
    def max_pending_connections(self) -> int: ...
    @property
    def requests_semaphore(self) -> Optional[Semaphore]: ...
    @property
    def connection_timeout(self) -> float: ...
    @property
    def workers(self) -> List[Worker]: ...
    @property
    def views(self) -> List[HTTPView]: ...
    @property
    def socket(self) -> _socket.socket: ...
    @property
    def middlewares(self) -> List[Middleware]: ...
    @property
    def listeners(self) -> List[Listener]: ...
    @property
    def routes(self) -> List[Route]: ...
    @property
    def resources(self) -> List[Resource]: ...
    @property
    def loop(self) -> asyncio.AbstractEventLoop: ...
    @loop.setter
    def loop(self, value: Any) -> None: ...
    @property
    def urls(self) -> Set[URL]: ...
    @property
    def paths(self) -> Set[str]: ...
    def url_for(self, path: str, *, is_websocket: bool=..., **kwargs: Any) -> URL: ...
    def inject(self, obj: Injectable) -> Any: ...
    def eject(self, obj: Injectable) -> Any: ...
    def is_closed(self) -> bool: ...
    def is_serving(self) -> bool: ...
    def is_ipv6(self) -> bool: ...
    def is_ssl(self) -> bool: ...
    def get_worker(self, id: int) -> Optional[Worker]: ...
    def add_worker(self, worker: Union[Worker, Any]) -> Worker: ...
    def start(self) -> None: ...
    def run(self): ...
    async def close(self) -> None: ...
    def websocket(self, path: str) -> Callable[[CoroFunc], WebsocketRoute]: ...
    def route(self, path: str, method: Optional[str]=...) -> Callable[[CoroFunc], Route]: ...
    def add_route(self, route: Union[Route, WebsocketRoute, Any]) -> Union[Route, WebsocketRoute]: ...
    def add_router(self, router: Union[Router, Any]) -> Router: ...
    def get(self, path: str) -> Callable[[CoroFunc], Route]: ...
    def put(self, path: str) -> Callable[[CoroFunc], Route]: ...
    def post(self, path: str) -> Callable[[CoroFunc], Route]: ...
    def delete(self, path: str) -> Callable[[CoroFunc], Route]: ...
    def head(self, path: str) -> Callable[[CoroFunc], Route]: ...
    def options(self, path: str) -> Callable[[CoroFunc], Route]: ...
    def patch(self, path: str) -> Callable[[CoroFunc], Route]: ...
    def remove_route(self, route: Union[Route, WebsocketRoute]) -> Union[Route, WebsocketRoute]: ...
    def add_event_listener(self, coro: CoroFunc, name: Optional[str]=...) -> Listener: ...
    def remove_event_listener(self, listener: Listener) -> Listener: ...
    def add_status_code_handler(
        self, 
        status: int, 
        callback: Callable[[Request, HTTPException, Union[PartialRoute, Route]], Coro]
    ) -> Callable[[Request, HTTPException, Union[PartialRoute, Route]], Coro]: ...
    def remove_status_code_handler(
        self, 
        status: int
    ) -> Callable[[Request, HTTPException, Union[PartialRoute, Route]], Coro]: ...
    def status_code_handler(
        self, 
        status: int
    ) -> Callable[[Callable[[Request, HTTPException, Union[PartialRoute, Route]], Coro]], 
        Callable[[Request, HTTPException, Union[PartialRoute, Route]], Coro]]: ... 
    def event(self, name: Optional[str]=...) -> Callable[[CoroFunc], Listener]: ...
    def dispatch(self, name: str, *args: Any, **kwargs: Any) -> Any: ...
    def add_view(self, view: Union[HTTPView, Any]) -> HTTPView: ...
    def remove_view(self, path: str) -> Optional[HTTPView]: ...
    def get_view(self, path: str) -> Optional[HTTPView]: ...
    def view(self, path: str) -> Any: ...
    def add_resource(self, resource: Union[Resource, Any]) -> Resource: ...
    def remove_resource(self, name: str) -> Optional[Resource]: ...
    def get_resource(self, name: str) -> Optional[Resource]: ...
    def resource(self, name: str=...) -> Callable[[Type[Resource]], Resource]: ...
    def add_middleware(self, callback: CoroFunc) -> Middleware: ...
    def middleware(self, callback: CoroFunc) -> Middleware: ...
    def remove_middleware(self, middleware: Middleware) -> Middleware: ...

def dualstack_ipv6(ipv4: str=..., ipv6: str=..., *, port: int=..., **kwargs: Any) -> Application: ...
