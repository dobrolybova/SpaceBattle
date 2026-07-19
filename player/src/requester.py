from aiohttp import ClientSession, ClientTimeout
from aiohttp.client import _RequestContextManager
from aiohttp.client_exceptions import ContentTypeError

from player.src.schemas import ResponseData


class Requester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = None

    def get_session(self, method, url, body, **kwargs) -> _RequestContextManager:
        if self.session is None or self.session.closed:
            self.session = ClientSession(
                timeout=ClientTimeout(total=1),
                base_url=self.base_url)
        return self.session.request(method=method, url=url, json=body, **kwargs)

    async def request(
            self, method="GET", url="", body=None, exc_by_status=True, **kwargs
    ) -> ResponseData:
        async with self.get_session(method, url, body, **kwargs) as response:
            try:
                js = await response.json()
            except ContentTypeError:
                text = await response.text()
                return ResponseData(status=response.status, text=text)
            if exc_by_status:
                response.raise_for_status()
            return ResponseData(status=response.status, json=js)
