import inspect
from typing import Callable, List, Dict, Optional, Tuple, Union
import re

from ._types import CoroFunc

from .errors import RegistrationError
from .objects import Route, WebsocketRoute


__all__ = (
    'Router',
)

class Router:
    """
    A route handler.

    Attributes:
        url_prefix: The prefix used for route urls.
        routes: A dictionary of routes.
        middlewares: A list of middleware callbacks.
    """
    _param_regex = r"{(?P<param>\w+)}"
    def __init__(self, url_prefix: str) -> None:
        """
        Router constructor.

        Args:
            url_prefix: The prefix used for route urls.
        """
        self.url_prefix = url_prefix
        self.routes: Dict[Tuple[str, str], Union[Route, WebsocketRoute]] = {}
        self.middlewares: List[CoroFunc] = []

    def _format_pattern(self, path: str):
        if not re.search(self._param_regex, path):
            return path

        regex = r""
        last_pos = 0

        for match in re.finditer(self._param_regex, path):
            regex += path[last_pos: match.start()]
            param = match.group("param")
            regex += r"(?P<%s>\w+)" % param
            last_pos = match.end()

        return regex

    def add_route(self, route: Union[Route, WebsocketRoute]) -> Union[Route, WebsocketRoute]:
        """
        Adds a route to the router.

        Args:
            route: The route to add.

        Returns:
            The route that was added.
        """
        path = self.url_prefix + route.path

        if isinstance(route, WebsocketRoute):
            self.routes[(path, route.method)] = route
            return route

        pattern = self._format_pattern(path)
        route.path = pattern

        self.routes[(route.path, route.method)] = route
        return route

    def remove_route(self, route: Union[Route, WebsocketRoute]) -> Optional[Union[Route, WebsocketRoute]]:
        """
        Removes a route from the router.

        Args:
            route: The route to remove.
        
        Returns:
            The route that was removed.
        """
        return self.routes.pop((route.path, route.method), None)

    def websocket(self, path: str) -> Callable[[CoroFunc], Route]:
        """
        A decorator for registering a websocket route.

        Args:
            path: The path to register the route to.
        """
        def wrapper(func: CoroFunc):
            route = WebsocketRoute(path, 'GET', func, router=self)
            self.add_route(route)

            return route
        return wrapper

    def route(self, path: str, method: str) -> Callable[[CoroFunc], Route]:
        """
        A decorator for registering a route.

        Args:
            path: The path to register the route to.
            method: The HTTP method to use for the route.
        """
        def wrapper(func: CoroFunc):
            route = Route(path, method, func, router=self)
            self.add_route(route)

            return route
        return wrapper

    def get(self, path: str) -> Callable[[CoroFunc], Route]:
        def wrapper(func: CoroFunc):
            route = Route(path, 'GET', func, router=self)
            self.add_route(route)

            return route
        return wrapper

    def post(self, path: str) -> Callable[[CoroFunc], Route]:
        def wrapper(func: CoroFunc):
            route = Route(path, 'POST', func, router=self)
            self.add_route(route)

            return route
        return wrapper

    def put(self, path: str) -> Callable[[CoroFunc], Route]:
        def wrapper(func: CoroFunc):
            route = Route(path, 'PUT', func, router=self)
            self.add_route(route)

            return route
        return wrapper

    def delete(self, path: str) -> Callable[[CoroFunc], Route]:
        def wrapper(func: CoroFunc):
            route = Route(path, 'DELETE', func, router=self)
            self.add_route(route)

            return route
        return wrapper

    def patch(self, path: str) -> Callable[[CoroFunc], Route]:
        def wrapper(func: CoroFunc):
            route = Route(path, 'PATCH', func, router=self)
            self.add_route(route)

            return route
        return wrapper

    def options(self, path: str) -> Callable[[CoroFunc], Route]:
        def wrapper(func: CoroFunc):
            route = Route(path, 'OPTIONS', func, router=self)
            self.add_route(route)

            return route
        return wrapper

    def head(self, path: str) -> Callable[[CoroFunc], Route]:
        def wrapper(func: CoroFunc):
            route = Route(path, 'HEAD', func, router=self)
            self.add_route(route)

            return route
        return wrapper

    def middleware(self, func: CoroFunc) -> CoroFunc:
        """
        A decorator for registering a middleware callback.

        Args:
            func: The middleware callback.
        
        Returns:
            The middleware callback.
        """
        if not inspect.iscoroutinefunction(func):
            raise RegistrationError('Middleware callbacks must be coroutine functions')

        self.middlewares.append(func)
        return func

    def __iter__(self):
        return self.routes.values().__iter__()