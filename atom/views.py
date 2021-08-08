from typing import Callable
import functools
import inspect

from .request import Request
from .objects import Route, WebsocketRoute
from .abc import AbstractRouter
from .utils import VALID_METHODS

__all__ = (
    'HTTPView',
    'ViewMeta'
)

class ViewMeta(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        attrs['__url_route__'] = kwargs.get('path', '')

        self = super().__new__(cls, name, bases, attrs)
        view_routes = []

        for base in self.mro():
            for elem, value in base.__dict__.items():
                if inspect.iscoroutinefunction(value):
                    if value.__name__.upper() in VALID_METHODS:
                        view_routes.append(value)

        self.__routes__ = view_routes
        return self

class HTTPView(metaclass=ViewMeta):
    def add_route(self, method: str, coro: Callable):
        setattr(self, method, coro)
        return coro

    def as_routes(self, router: AbstractRouter):
        routes = []

        for coro in self.__routes__:
            actual = functools.partial(coro, self)

            route = Route(self.__url_route__, coro.__name__.upper(), actual, router=router)
            router.add_route(route)
            
        return routes
