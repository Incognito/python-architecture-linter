from modular_provider_architecture.logic_module.logic import Logic


class LogicProvider:
    def provide_logic_one(self) -> Logic:
        return self._create_logic(1)

    def provide_logic_two(self) -> Logic:
        return self._create_logic(2)

    def _create_logic(self, variation) -> Logic:
        return Logic(variation)
