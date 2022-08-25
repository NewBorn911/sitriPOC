from __future__ import annotations

import typing

import hvac
import pytest
from pydantic import BaseModel, Field

from sitri.providers.contrib.vault import VaultKVConfigProvider
from sitri.settings.contrib.vault import VaultKVSettings

from .mock import VaultClientMock

T = typing.TypeVar("T", bound=VaultKVSettings)


@pytest.fixture(scope="module")
def vault_connection() -> typing.Callable[[], VaultClientMock]:
    """vault_connection.

    :rtype: typing.Callable
    """
    return lambda: VaultClientMock()


@pytest.fixture(scope="module")
def vault_kv_config(vault_connection: typing.Callable[[], hvac.Client]) -> VaultKVConfigProvider:
    """vault_kv_config.

    :param vault_connection:
    :rtype: VaultKVConfigProvider
    """
    return VaultKVConfigProvider(vault_connector=vault_connection, mount_point="test", secret_path="test")  # noqa


@pytest.fixture(scope="module")
def vault_kv_settings_empty(vault_kv_config: VaultKVConfigProvider) -> type[T]:
    """vault_kv_settings_empty.

    :param vault_kv_config:
    """

    class TestSettings(VaultKVSettings):
        """TestSettings."""

        class Config(VaultKVSettings.VaultKVSettingsConfig):
            """Config."""

            provider = vault_kv_config

    return TestSettings


@pytest.fixture(scope="module")
def vault_kv_settings() -> typing.Callable[[VaultKVConfigProvider], type[T]]:
    """vault_kv_settings."""

    def wrapper(provider_instance: VaultKVConfigProvider) -> type[T]:
        """wrapper.

        :param provider_instance:
        """

        class TestSettings(VaultKVSettings):
            """TestSettings."""

            key1: str = Field(...)
            key2: str = Field(...)

            class Config(VaultKVSettings.VaultKVSettingsConfig):
                """Config."""

                provider = provider_instance

        return TestSettings

    return wrapper


@pytest.fixture(scope="module")
def vault_kv_settings_vault_raise() -> typing.Callable[[VaultKVConfigProvider], type[T]]:
    """vault_kv_settings_vault_raise."""

    def wrapper(provider_instance: VaultKVConfigProvider) -> type[T]:
        """wrapper.

        :param provider_instance:
        """

        class TestSettings(VaultKVSettings):
            """TestSettings."""

            key3: str = Field(...)

            class Config(VaultKVSettings.VaultKVSettingsConfig):
                """Config."""

                provider = provider_instance

        return TestSettings

    return wrapper


@pytest.fixture(scope="module")
def vault_kv_settings_complex() -> typing.Callable[[VaultKVConfigProvider], type[T]]:
    """vault_kv_settings_complex."""

    def wrapper(provider_instance: VaultKVConfigProvider) -> type[T]:
        """wrapper.

        :param provider_instance:
        """

        class Key0Model(BaseModel):
            """Key0Model."""

            test: str = Field(...)

        class TestSettings(VaultKVSettings):
            """TestSettings."""

            key0: Key0Model = Field(...)

            class Config(VaultKVSettings.VaultKVSettingsConfig):
                """Config."""

                provider = provider_instance

        return TestSettings

    return wrapper


@pytest.fixture(scope="module")
def vault_kv_settings_complex_raise() -> typing.Callable[[VaultKVConfigProvider], type[T]]:
    """vault_kv_settings_complex_raise."""

    def wrapper(provider_instance: VaultKVConfigProvider) -> type[T]:
        """wrapper.

        :param provider_instance:
        """

        class Key4Model(BaseModel):
            """Key4Model."""

            test: str = Field(...)

        class TestSettings(VaultKVSettings):
            """TestSettings."""

            key4: Key4Model = Field(...)

            class Config(VaultKVSettings.VaultKVSettingsConfig):
                """Config."""

                provider = provider_instance

        return TestSettings

    return wrapper


@pytest.fixture(scope="module")
def path_to_json() -> str:
    """path_to_json.

    :rtype: str
    """
    return "tests/unit/settings/vault_kv/data.json"


@pytest.fixture(scope="module")
def vault_kv_local_mode(path_to_json: str) -> typing.Callable[[VaultKVConfigProvider], type[T]]:
    """vault_kv_local_mode.

    :param path_to_json:
    """

    def wrapper(provider_instance: VaultKVConfigProvider) -> type[T]:
        """wrapper.

        :param provider_instance:
        """

        class Key4Model(BaseModel):
            """Key4Model."""

            test: str = Field(...)

        class TestSettings(VaultKVSettings):
            """TestSettings."""

            key1: str = Field(...)
            key2: str = Field(...)
            key3: str = Field(...)
            key4: Key4Model = Field(...)

            class Config(VaultKVSettings.VaultKVSettingsConfig):
                """Config."""

                provider = provider_instance

                local_mode = True
                local_provider_args = {"json_path": path_to_json}
                local_mode_path_prefix = "test"

        return TestSettings

    return wrapper
