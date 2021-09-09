import enum
from typing import Any, Callable, Coroutine, Dict, Optional, Tuple

class WebSocketOpcode(enum.IntEnum):
    CONTINUATION: int = ...
    TEXT: int = ...
    BINARY: int = ...
    CLOSE: int = ...
    PING: int = ...
    PONG: int = ...

class WebSocketCloseCode(enum.IntEnum):
    NORMAL: int = ...
    GOING_AWAY: int = ...
    PROTOCOL_ERROR: int = ...
    UNSUPPORTED: int = ...
    RESERVED: int = ...
    NO_STATUS: int = ...
    ABNORMAL: int = ...
    UNSUPPORTED_PAYLOAD: int = ...
    POLICY_VIOLATION: int = ...
    TOO_LARGE: int = ...
    MANDATORY_EXTENSION: int = ...
    INTERNAL_ERROR: int = ...
    SERVICE_RESTART: int = ...
    TRY_AGAIN_LATER: int = ...
    BAD_GATEWAY: int = ...
    TLS_HANDSHAKE: int = ...

class Data:
    raw: bytearray = ...
    frame: WebSocketFrame = ...
    def __init__(self, raw: bytearray, frame: WebSocketFrame) -> None: ...
    @property
    def opcode(self) -> WebSocketOpcode: ...
    @property
    def data(self) -> bytes: ...
    def encode(self, opcode: Optional[WebSocketOpcode]=..., *, masked: bool=...) -> bytes: ...
    def as_string(self) -> str: ...
    def as_json(self) -> Dict[str, Any]: ...

class WebSocketFrame:
    SHORT_LENGTH: Any = ...
    LONGLONG_LENGTH: Any = ...
    opcode: WebSocketOpcode = ...
    fin: bool = ...
    rsv1: bool = ...
    rsv2: bool = ...
    rsv3: bool = ...
    data: bytes = ...
    def __init__(self, opcode: WebSocketOpcode, *, fin: bool=..., rsv1: bool=..., rsv2: bool=..., rsv3: bool=..., data: bytes) -> None: ...
    @staticmethod
    def mask(data: bytes, mask: bytes) -> bytes: ...
    def encode(self, masked: bool=...) -> bytearray: ...
    @classmethod
    async def decode(cls: Any, read: Callable[[int], Coroutine[None, None, bytes]], mask: bool=...) -> Tuple[WebSocketOpcode, bytearray, WebSocketFrame]: ...
