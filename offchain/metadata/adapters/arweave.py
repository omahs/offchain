import random
from typing import Optional

import httpx
from requests import PreparedRequest, Response
from urllib3.util import parse_url

from offchain.metadata.adapters.base_adapter import HTTPAdapter
from offchain.metadata.registries.adapter_registry import AdapterRegistry


@AdapterRegistry.register
class ARWeaveAdapter(HTTPAdapter):
    """Provides an interface for Requests sessions to contact ARWeave urls.

    Args:
        host_prefixes (list[str], optional): list of possible host url prefixes to choose from
        key (str, optional): optional key to send with request
        secret (str, optional): optional secret to send with request
        timeout (int): request timeout in seconds. Defaults to 10 seconds.
    """

    def __init__(
        self,
        host_prefixes: Optional[list[str]] = None,
        key: Optional[str] = None,
        secret: Optional[str] = None,
        timeout: int = 10,
        *args,
        **kwargs,
    ):
        self.host_prefixes = host_prefixes or ["https://arweave.net/"]

        assert all(
            [g.endswith("/") for g in self.host_prefixes]
        ), "gateways should have trailing slashes"

        self.key = key
        self.secret = secret
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def parse_ar_url(self, url: str) -> str:
        """Format and send async request to ARWeave host.

        Args:
            url (str): url to send request to
            sess (httpx.AsyncClient()): async client

        Returns:
            httpx.Response: response from ARWeave host.
        """
        parsed = parse_url(url)
        if parsed.scheme == "ar":
            gateway = random.choice(self.host_prefixes)
            new_url = f"{gateway}{parsed.host}"
            if parsed.path is not None:
                new_url += parsed.path
            url = new_url
        return url

    async def gen_send(self, url: str, sess: httpx.AsyncClient(), *args, **kwargs) -> httpx.Response:
        """Format and send async request to ARWeave host.

        Args:
            url (str): url to send request to
            sess (httpx.AsyncClient()): async client

        Returns:
            httpx.Response: response from ARWeave host.
        """
        return await sess.get(self.parse_ar_url(url), timeout=self.timeout, follow_redirects=True)

    def send(self, request: PreparedRequest, *args, **kwargs) -> Response:
        """Format and send request to ARWeave host.

        Args:
            request (PreparedRequest): incoming request

        Returns:
            Response: response from ARWeave host.
        """
        request.url = self.parse_ar_url(request.url)
        kwargs["timeout"] = self.timeout
        return super().send(request, *args, **kwargs)

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        """Format and send async request to ARWeave host.

        Args:
            request (httpx.Request): httpx request

        Returns:
            httpx.Response: response from ARWeave host.
        """
        host = request.url.host.replace(request.url.host, self.host_prefixes[0])
        request.url = httpx.URL(host[:-1] + request.url.path)
        return await httpx.AsyncClient(timeout=self.timeout).send(request, follow_redirects=True)