from typing import Protocol, Union

from offchain.metadata.adapters.base_adapter import Adapter


class BaseFetcher(Protocol):
    """Base protocol for fetcher classes

    Attributes:
        timeout (int): request timeout in seconds.
        max_retries (int): maximum number of request retries.
    """

    timeout: int
    max_retries: int

    def __init__(self, timeout: int, max_retries: int) -> None:
        pass

    def set_timeout(self, new_timeout: int):
        """Setter function for timeout

        Args:
            new_timeout (int): new request timeout in seconds.
        """
        pass

    def set_max_retries(self, new_max_retries: int):
        """Setter function for max retries

        Args:
            new_max_retries (int): new maximum number of request retries.
        """
        pass

    def register_adapter(self, adapter: Adapter, url_prefix: str):
        """Register an adapter to a url prefix.

        Args:
            adapter (Adapter): an Adapter instance to register.
            url_prefix (str): the url prefix to which the adapter should be registered.
        """
        pass

    def register_async_adapter(self, async_adapters: dict):
        """Register adapters to a url prefix for async session.

        Args:
            async_adapters (dict): dictionary of adapters and prefixes to register
        """
        pass

    def fetch_mime_type_and_size(self, uri: str) -> tuple[str, int]:
        """Fetch the mime type and size of the content at a given uri.

        Args:
            uri (str): uri from which to fetch content mime type and size.

        Returns:
            tuple[str, int]: mime type and size
        """
        pass

    def fetch_content(self, uri: str) -> Union[dict, str]:
        """Fetch the content at a given uri

        Args:
            uri (str): uri from which to fetch content.

        Returns:
            Union[dict, str]: content fetched from uri
        """
        pass

    async def gen_fetch_content(self, uri: str) -> Union[dict, str]:
        """Async fetch the content at a given uri

        Args:
            uri (str): uri from which to fetch content.

        Returns:
            Union[dict, str]: content fetched from uri
        """
        pass
