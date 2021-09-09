"""
MIT License

Copyright (c) 2021 blanketsucks

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from typing import Dict, Union, Optional, TypedDict
import importlib
import os
import pathlib
import ssl
import multiprocessing

from .utils import LOCALHOST, LOCALHOST_V6, SETTING_ENV_PREFIX, is_ipv6

__all__ = (
    'Settings',
    'DEFAULT_SETTINGS',
    'settings_from_file',
    'settings_from_env',
    'VALID_SETTINGS',
)

VALID_SETTINGS = (
    'host',
    'port',
    'use_ipv6',
    'ssl_context',
    'worker_count'
)

DEFAULT_SETTINGS = {
    'host': LOCALHOST,
    'port': 8080,
    'use_ipv6': False,
    'ssl_context': None,
    'worker_count': (multiprocessing.cpu_count() * 2) + 1,
    'session_cookie_name': None,
}

class Settings(TypedDict):
    """
    A :class:`typing.TypedDict` representing settings used by the application.

    Attributes
    ----------
    host: :class:`str`
        The hostname or IP address to listen on.
    port: :class:`int`
        The port to listen on.
    use_ipv6: :class:`bool`
        Whether to use IPv6.
    ssl_context: Optional[:class:`ssl.SSLContext`]
        The SSL context to use.
    worker_count: :class:`int`
        The number of workers to use.
    """
    host: str
    port: int
    use_ipv6: bool
    ssl_context: Optional[ssl.SSLContext]
    worker_count: int
    session_cookie_name: Optional[str]

def settings_from_file(path: Union[str, pathlib.Path]) -> Settings:
    """
    Loads settings from a file.

    Parameters
    ----------
    path: Union[:class:`str`, :class:`pathlib.Path`]
        The path of the file to load settings from.
    """
    if isinstance(path, pathlib.Path):
        path = str(path)

    module = importlib.import_module(path)

    kwargs = {}
    
    for key, default in DEFAULT_SETTINGS.items():
        value = getattr(module, key.casefold(), default)
        kwargs[key] = value

    if kwargs['use_ipv6'] and not is_ipv6(kwargs['host']):
        kwargs['host'] = LOCALHOST_V6

    settings = Settings(**kwargs)
    return settings

def settings_from_env() -> Settings:
    """
    Loads settings from environment variables.

    Returns:
        A [Settings](./settings.md) object.
    """
    env = os.environ
    kwargs = {}

    for key, default in DEFAULT_SETTINGS.items():
        item = SETTING_ENV_PREFIX + key.casefold()
        kwargs[key] = env.get(item, default)

    if kwargs['use_ipv6'] and not is_ipv6(kwargs['host']):
        kwargs['host'] = LOCALHOST_V6

    settings = Settings(**kwargs)
    return settings
