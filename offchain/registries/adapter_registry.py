from typing import Optional, Type

from offchain.adapters.base_adapter import Adapter
from offchain.registries.base_registry import BaseRegistry


class AdapterRegistry(BaseRegistry):
    __adapter_registry: dict[str, Adapter] = {}

    @staticmethod
    def get_all() -> list[Adapter]:
        return list(AdapterRegistry.__adapter_registry.values())

    @staticmethod
    def get_adapter_cls_by_name(adapter_name: str) -> Optional[Adapter]:
        return AdapterRegistry.__adapter_registry.get(adapter_name)

    @staticmethod
    def validate(adapter_cls: Type[Adapter]):
        assert (
            adapter_cls.__name__ not in AdapterRegistry.__adapter_registry
        ), f"{adapter_cls.__name__} already exists in registry."

    @staticmethod
    def add(adapter_cls: Type[Adapter]):
        AdapterRegistry.__adapter_registry[adapter_cls.__name__] = adapter_cls