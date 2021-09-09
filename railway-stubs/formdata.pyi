from .file import File
from .request import Request
from typing import Any, List, Optional, Tuple, TypeVar

T = TypeVar('T')

class Disposition:
    header: str = ...
    def __init__(self, header: str) -> None: ...
    @property
    def content_type(self) -> str: ...
    @property
    def name(self) -> Optional[str]: ...
    @property
    def filename(self) -> Optional[str]: ...

class FormData:
    files: List[Tuple[File, Disposition]] = ...
    def __init__(self) -> None: ...
    def __iter__(self) -> Any: ...
    def add_file(self, file: File, disposition: Optional[Disposition]) -> None: ...
    @classmethod
    def from_request(cls: Any, request: Request) -> FormData: ...
