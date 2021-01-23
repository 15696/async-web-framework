
from .error import HTTPNotFound, HTTPBadRequest
import re
import typing

class URLRouter:
    _param_regex = r"{(?P<param>\w+)}"

    def __init__(self) -> None:
        self._routes: typing.Dict[typing.Tuple[str, str], typing.Coroutine] = {}

    def resolve(self, request):
        for (method, pattern), handler in self._routes.items():
            match = re.match(pattern, request.url.raw_path)

            if match is None:
                key = (request.method, request.url.raw_path)
                value = self._routes.get(key)

                if value is None:
                    raise HTTPNotFound(reason=f"Could not find {request.url.raw_path!r}")

                return {}, value

            if method != request.method:
                raise HTTPBadRequest(reason=f"{request.method!r} is not allowed for {request.url.raw_path!r}")

            return match.groupdict(), handler
            
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

    def add_route(self, route):
        pattern = self._format_pattern(route.path)
        print(pattern)
        self._routes[(route.method, pattern)] = route.coro

    def remove_route(self, method: str, path: str):
        coro = self._routes.pop((method, path))
        return coro
