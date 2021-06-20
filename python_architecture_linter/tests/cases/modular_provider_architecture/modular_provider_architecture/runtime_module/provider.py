from functools import cache

from modular_provider_architecture.logic_module.logic import Logic
from modular_provider_architecture.logic_module.provider import LogicProvider

from .runtime import Runtime


class RuntimeProvider:
    def provide_runtime(self) -> Runtime:
        logic_one = self._provide_logic_one()
        logic_two = self._provide_logic_two()

        return Runtime([logic_one, logic_two])

    def _provide_logic_one(self) -> Logic:
        return self._provide_logic_provider().provide_logic_one()

    def _provide_logic_two(self) -> Logic:
        return self._provide_logic_provider().provide_logic_two()

    @cache
    def _provide_logic_provider(self) -> LogicProvider:
        return LogicProvider()
