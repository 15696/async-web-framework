from typing import Any
from . import http
from .app import Application

__all__ = (
    'TestClient',
)

class TestClient:
    """
    Test client for the application.

    Attributes:
        app: The application to test.
        session: The HTTP session used.
    """
    def __init__(self, app: Application) -> None:
        """
        
        """
        self.app: Application = app
        self.session: http.HTTPSession = http.HTTPSession()

    @property
    def host(self) -> str:
        return self.app.host

    @property
    def port(self) -> int:
        return self.app.port

    def ws_connect(self, path: str) -> http.AsyncContextManager[http.Websocket]:
        """
        Performs a websocket connection.

        Args:
            path: The path to the websocket.

        Returns:
            A context manager for the websocket.

        Example:
            ```py
            import railway

            app = railway.Application()
            client = railway.TestClient(app)

            @app.websocket('/ws')
            async def handler(request: railway.Request, ws: railway.Websocket):
                await ws.send(b'Hello!')

                data = await ws.recieve()
                print(data.data)

                await ws.close()

            async def main():
                async with app:
                    async with client.ws_connect('/ws') as ws:
                        message = await ws.recieve_str()
                        print(message)

                        await ws.send(b'Hi!')
            
            app.loop.run_until_complete(main())
            ```
        """
        url = self.app.url_for(path, is_websocket=True)
        return self.session.ws_connect(url)

    def request(self, path: str, method: str, **kwargs: Any) -> http.AsyncContextManager[http.HTTPResponse]:
        """
        Sends a request to the application.

        Args:
            path: The path to the resource.
            method: The HTTP method.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            A context manager for the request.

        Example:
            ```py
            import railway

            app = railway.Application()
            client = railway.TestClient(app)

            @app.route('/')
            async def index(request: railway.Request):
                return 'another creative response'

            async def main():
                async with app:
                    async with client.get('/') as response:
                        print(response.status)
                        text = await response.text()

                        print(text)

            app.loop.run_until_complete(main())
            ```
        
        """
        url = self.app.url_for(path)
        return self.session.request(url=url, method=method, **kwargs)

    def get(self, path: str, **kwargs: Any):
        return self.request(path, 'GET', **kwargs)

    def post(self, path: str, **kwargs: Any):
        return self.request(path, 'POST', **kwargs)

    def put(self, path: str, **kwargs: Any):
        return self.request(path, 'PUT', **kwargs)

    def delete(self, path: str, **kwargs: Any):
        return self.request(path, 'DELETE', **kwargs)


    