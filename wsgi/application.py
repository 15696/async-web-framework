
from .request import Request
from .error import HTTPException
from .server import Server
from .router import Router
from .listeners import ListenersHandler
from .response import Response
from .helpers import format_exception, jsonify
from .tasks import Task
from .settings import Settings
from .objects import Route, Listener, Middleware

import asyncio
import json
import functools
import inspect
import typing

import jwt
import datetime


class Application:
    """
    
    ## Listeners order

    `on_startup` -> `on_connection_made` -> `on_request` -> `on_socket_receive` -> `on_connection_lost` -> `on_shutdown`
    
    """
    def __init__(self, routes: typing.List[Route]=None,
                listeners: typing.List[Listener]=None,
                middlewares: typing.List[Middleware]=None, *,
                loop: asyncio.AbstractEventLoop=None) -> None:

        self.loop = loop or asyncio.get_event_loop()
        self.settings = Settings()

        self._router = Router()
        self._listener = ListenersHandler()

        self._middlewares: typing.List[typing.Coroutine] = []
        self._tasks: typing.List[Task] = []

        self._load_from_arguments(routes=routes, listeners=listeners, middlewares=middlewares)

    def make_server(self, cls=Server):
        res = cls(self.loop, app=self, handler=self._handler)
        return res
        
    def get_setting(self, key: str):
        value = self.settings.get(key, None)
        return value

    def remove_setting(self, key: str):
        value = self.settings.pop(key)
        return value

    @property
    def router(self):
        return self._router

    @property
    def listener_handler(self):
        return self._listener

    @property
    def middlewares(self):
        return self._middlewares

    @property
    def listeners(self):
        return self._listener.listeners

    @property
    def routes(self):
        return self._router.routes

    @property
    def tasks(self):
        return self._tasks

    def task(self, *, seconds=0, minutes=0, hours=0, count=None, loop=None):
        def wrapper(func):
            cls = Task(
                func,
                seconds,
                minutes,
                hours,
                count,
                loop
            )

            self._tasks.append(cls)
            return cls
        return wrapper

    def _load_from_arguments(self, routes: typing.List[Route]=None, listeners: typing.List[Listener]=None, 
                            middlewares: typing.List[Middleware]=None):

        if routes:
            for route in routes:
                self.add_route(route)

        if listeners:
            for listener in listeners:
                coro = listener.coro
                name = listener.event

                self.add_listener(coro, name)

        if middlewares:
            for middleware in middlewares:
                coro = middleware.coro
                self.add_middleware(coro)

    # Running the app

    async def start(self, host: str=None, *, port: int=None):
        for task in self._tasks:
            task.start()

        if not host:
            host = '127.0.0.1'

        if not port:
            port = 8080

        serv = self.make_server()
        server: asyncio.AbstractServer = await self.loop.create_server(lambda: serv, host=host, port=port)

        await self.dispatch('on_startup', host, port)

        try:
            await server.serve_forever()
        except KeyboardInterrupt:
            await self.dispatch('on_shutdown')
            server.close()

            await server.wait_closed()
            self.loop.stop()

    def run(self, host: str=None, *, port: int=None):
        for task in self._tasks:
            task.start()

        if not host:
            host = '127.0.0.1'

        if not port:
            port = 8080

        serv = self.make_server()

        server = self.loop.run_until_complete(
            self.loop.create_server(lambda: serv, host=host, port=port)
        )
        self.loop.run_until_complete(self.dispatch('on_startup', host, port))

        try:
            self.loop.run_until_complete(server.serve_forever())
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.dispatch('on_shutdown'))
            server.close()
            
            self.loop.run_until_complete(server.wait_closed())
            self.loop.stop()

    # Route handler 

    async def _handler(self, request: Request, response_writer):
        try:
            info, handler = self._router.resolve(request)
            request._args = info

            if len(self._middlewares) != 0:
                for middleware in self._middlewares:
                    handler = functools.partial(middleware, handler=handler)
                
            resp = await handler(request)

            if isinstance(resp, dict) or isinstance(resp, list):
                data = json.dumps(resp)
                resp = Response(data, content_type='application/json')

            if isinstance(resp, str):
                resp = Response(resp)

        except HTTPException as exc:
            await self.dispatch('on_error', exc)
            resp = exc

        except Exception as exc:
            await self.dispatch('on_error', exc)
            resp = format_exception(exc)

        response_writer(resp)

    # Routing

    def add_route(self, route: Route):
        if not inspect.iscoroutinefunction(route.coro):
            raise RuntimeError('Routes must be async.')

        self._router.add_route(route)
        return route

    def remove_route(self, path: str, method: str):
        return self._router.remove_route(method, path)

    def route(self, path: str, method: str):
        def decorator(func: typing.Coroutine):
            route = Route(path, method, func)
            return self.add_route(route)

        return decorator

    def get(self, path: str):
        def decorator(func: typing.Coroutine):
            route = Route(path, 'GET', func)
            self.add_route(route)

            return route
        return decorator

    def put(self, path: str):
        def decorator(func: typing.Coroutine):
            route = Route(path, 'PUT', func)
            self.add_route(route)

            return route
        return decorator

    def post(self, path: str):
        def decorator(func: typing.Coroutine):
            route = Route(path, 'POST', func)
            self.add_route(route)

            return route
        return decorator

    def delete(self, path: str):
        def decorator(func: typing.Coroutine):
            route = Route(path, 'DELETE', func)
            self.add_route(route)

            return route
        return decorator

    def add_protected_route(self, path: str, method: str, coro: typing.Coroutine):
        async def func(request: Request):
            _type, token = self.get_oauth_token(request.headers)
            valid = self.validate_token(token)

            if not valid:
                return jsonify(message='Invalid Token.', status=403)

            return coro(request)

        route = Route(path, method, func)
        return self.add_route(route)

    def protected(self, path: str, method: str):
        def decorator(func: typing.Coroutine):
            return self.add_protected_route(path, method, func)
        return decorator

    def generate_oauth2_token(self, client_id: str, client_secret: str, *, validator: typing.Coroutine=None, expires: int=60):
        if validator:
            self.loop.run_until_complete(validator(client_secret))

        secret_key = self.get_setting('SECRET_KEY')
        data = {
            'user' : client_id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=expires)
        }
    
        token = jwt.encode(data, secret_key)
        return token

    def get_oauth_token(self, headers: typing.Dict[str, str]):
        auth = headers.get('Authorization')

        if not auth:
            return None

        _type, token = auth.split(' ')
        return _type, token

    def validate_token(self, token: str):
        secret = self.get_setting('SECRET_KEY')

        try:
            data = jwt.decode(token, secret)
        except:
            return False

        return True

    def add_oauth2_login_route(self, path: str, method: str, coro: typing.Coroutine=None,
                               validator: typing.Coroutine=None, expires: int=60):

        async def func(req: Request):
            client_id = req.headers.get('client_id')
            client_secret = req.headers.get('client_secret')

            if client_id and client_secret:
                token = self.generate_oauth2_token(client_id, client_secret,
                                                   validator=validator, expires=expires)

                if coro:
                    return await coro(req, token)
                
                return jsonify(access_token=token)

            if not client_secret or not client_id:
                return jsonify(message='Missing client_id or client_secret.', status=403)

        route = Route(path, method, func)
        return self.add_route(route)

    def oauth2(self, path: str, method: str, validator: typing.Coroutine=None, expires: int=60):
        def decorator(func):
            return self.add_oauth2_login_route(path, method, func, validator=validator, expires=expires)
        return decorator

    # Listeners

    def add_listener(self, f: typing.Coroutine, name: str=None) -> Listener:
        if not inspect.iscoroutinefunction(f):
            raise RuntimeError('All listeners must be async')
        
        return self._listener.add_listener(f, name)


    def remove_listener(self, func: typing.Coroutine=None, name: str=None):
        return self._listener.remove_listener(func, name)

    def listen(self, name: str=None):
        def decorator(func: typing.Coroutine):
            return self.add_listener(func, name)
        return decorator

    async def dispatch(self, name: str, *args, **kwargs):
        try:
            listeners = self._listener.listeners[name]
        except KeyError:
            return
        
        for listener in listeners:
            await listener(*args, **kwargs)

        return listeners

    # Middlewares

    def middleware(self):
        def wrapper(func: typing.Coroutine):
            return self.add_middleware(func)
        return wrapper

    def add_middleware(self, middleware: typing.Coroutine):
        if not inspect.iscoroutinefunction(middleware):
            raise RuntimeError('All middlewares must be async')

        self._middlewares.append(middleware)
        return Middleware(middleware)

    def remove_middleware(self, middleware: typing.Coroutine) -> typing.Coroutine:
        self._middlewares.remove(middleware)
        return middleware

