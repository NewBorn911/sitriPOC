"""
.. module:: config.providers
   :synopsis: Config Base
.. moduleauthor:: Aleksander Lavrov <github.com/egnod>
"""
import inspect
import typing
from abc import ABC, abstractmethod

from sitri.logger import get_default_logger


class ConfigProvider(ABC):
    """Base class for config providers."""

    def __init__(self, logger: typing.Any | None = None, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Default init method for all providers."""

        if not logger:
            logger = get_default_logger(__name__)

        self.logger = logger

    @property
    @abstractmethod
    def provider_code(self) -> str:
        """Provider code property for identity provider in manager."""

    @abstractmethod
    def get(self, key: str, **kwargs: typing.Any) -> typing.Any | None:
        """Get value from storage.

        :param key: key for find value in provider source
        :param kwargs: additional arguments for providers
        """

    @abstractmethod
    def keys(self, **kwargs: typing.Any) -> list[str]:
        """Get keys list in storage."""

    def fill(self, call: typing.Callable[[typing.Any], typing.Any], **kwargs: typing.Any) -> typing.Any:
        """Fill callable object kwargs if all founded by provider.

        :param call: callable object for fill
        :param kwargs: additional arguments for getting
        """
        parameters = inspect.signature(call).parameters
        data = {}

        for key in parameters.keys():
            data[key] = self.get(key=key, **kwargs)

        return call(**data)


class ConfigProviderManager:
    """Manager for children ConfigProvider classes."""

    @staticmethod
    def get_by_code(code: str) -> type[ConfigProvider] | None:
        """Get config provider by provider_code.

        :param code: provider_code for search config provider
        :Example:
            .. code-block:: python

               ConfigProviderManager.get_by_code("system")
        """
        for provider in ConfigProvider.__subclasses__():
            if provider.provider_code == code:  # type: ignore
                return provider
        return None
