import asyncio
import pathlib
import socket
import sys
import ssl
from railway.streams import StreamTransport
from railway._types import peer
from typing import Any, Dict, List, Optional, Tuple, Union


class ServerProtocol(asyncio.Protocol):
    loop: asyncio.AbstractEventLoop = ...
    transport: StreamTransport = ...
    pending: asyncio.Queue[Tuple[StreamTransport, asyncio.Future[None]]] = ...
    def __init__(self, loop: asyncio.AbstractEventLoop, max_connections: Optional[int]) -> None: ...
    def __call__(self): ...
    def connection_made(self, transport: asyncio.Transport) -> None: ...
    def connection_lost(self, exc: Optional[Exception]) -> None: ...
    def get_waiter(self, peername: Tuple[str, int]) -> Optional[asyncio.Future[None]]: ...
    def data_received(self, data: bytes) -> None: ...
    def pause_writing(self) -> None: ...
    def resume_writing(self) -> None: ...
    def eof_received(self) -> None: ...

class ClientConnection:
    loop: asyncio.AbstractEventLoop = ...
    def __init__(self, protocol: ServerProtocol, transport: StreamTransport, loop: asyncio.AbstractEventLoop) -> None: ...
    async def __aenter__(self): ...
    async def __aexit__(self, *args: Any) -> None: ...
    @property
    def protocol(self) -> ServerProtocol: ...
    @property
    def peername(self) -> Tuple[str, int]: ...
    @property
    def sockname(self) -> Tuple[str, int]: ...
    def is_closed(self) -> bool: ...
    async def receive(self, nbytes: Optional[int]=..., *, timeout: Optional[int]=...) -> bytes: ...
    async def write(self, data: bytes) -> int: ...
    async def writelines(self, data: List[bytes]) -> int: ...
    async def sendfile(self, path: Union[str, pathlib.Path], *, offset: int=..., count: Optional[int]=..., fallback: bool=...) -> int: ...
    async def close(self) -> None: ...
    def __aiter__(self): ...
    async def __anext__(self): ...

class BaseServer:
    loop: asyncio.AbstractEventLoop = ...
    max_connections: int = ...
    def __init__(self, *, max_connections: Optional[int]=..., loop: Optional[asyncio.AbstractEventLoop]=..., is_ssl: Optional[bool]=..., ssl_context: Optional[ssl.SSLContext]=...) -> None: ...
    def create_ssl_context(self) -> ssl.SSLContext: ...
    def is_ssl(self) -> bool: ...
    def is_serving(self) -> bool: ...
    def is_closed(self) -> bool: ...
    async def __aenter__(self): ...
    async def __aexit__(self, *exc: Any) -> Any: ...
    async def serve(self) -> asyncio.Future[None]: ...
    async def close(self) -> None: ...
    async def accept(self, *, timeout: Optional[int]=...) -> ClientConnection: ...

class TCPServer(BaseServer):
    host: str = ...
    port: str = ...
    ipv6: bool = ...
    def __init__(self, host: Optional[str]=..., port: Optional[int]=..., *, ipv6: bool=..., max_connections: Optional[int]=..., loop: Optional[asyncio.AbstractEventLoop]=..., is_ssl: Optional[bool]=..., ssl_context: Optional[ssl.SSLContext]=...) -> None: ...
    async def serve(self, sock: Optional[socket.socket]=...) -> asyncio.Future[None]: ...

if sys.platform != 'win32':
    class UnixServer(BaseServer):
        path: str = ...
        def __init__(self, path: Optional[str]=..., *, max_connections: Optional[int]=..., loop: Optional[asyncio.AbstractEventLoop]=..., is_ssl: Optional[bool]=..., ssl_context: Optional[ssl.SSLContext]=...) -> None: ...
        async def serve(self, sock: Optional[socket.socket]=...) -> asyncio.Future[None]: ...
    
    def create_unix_server(path: str, *, max_connections: Optional[int]=..., loop: Optional[asyncio.AbstractEventLoop]=..., is_ssl: Optional[bool]=..., ssl_context: Optional[ssl.SSLContext]=...) -> UnixServer: ...

def create_server(host: Optional[str]=..., port: Optional[int]=..., *, ipv6: bool=..., max_connections: Optional[int]=..., loop: Optional[asyncio.AbstractEventLoop]=..., is_ssl: bool=..., ssl_context: Optional[ssl.SSLContext]=...) -> TCPServer: ...
