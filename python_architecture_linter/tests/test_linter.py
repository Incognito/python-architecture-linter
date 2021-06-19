from python_architecture_linter.lint_provider_class import linter


def test_method_violations():
    class_node = """
    class RuntimeProvider:
        def __init__(self):
            pass

        def provide_entrypoint(self) -> Entrypoint:
            return Entrypoint(consumer=self._provide_consumer(), pipeline=self._provide_gps_pipeline())

        def _provide_consumer(self) -> RuntimeConsumer:
            return self._provide_gps_consumer_provider().provide_consumer()

        def _create_foo(self) -> PipelineInterface:
            return self._provide_gps_pipeline_provider().provide_gps_pipeline()

        def create_foo(self) -> GpsPipelineProvider: # violation
            return GpsPipelineProvider()

        def bar(self) -> GpsConsumerProvider: # violation
            return GpsConsumerProvider()

        def _bar(self) -> GpsConsumerProvider: # violation
            return GpsConsumerProvider()

        def _provide_bad_bar_with_arg(self, badarg) -> GpsConsumerProvider: # violation
            foo = self._create_foo()
            return GpsConsumerProvider(foo)

        def _provide_bar(self) -> GpsConsumerProvider:
            foo = self._create_foo()
            return GpsConsumerProvider(foo)

        def _provide_some_logic(self) -> GpsConsumerProvider:
            foo = self._create_foo()
            if foo: # violation
                pass

            return GpsConsumerProvider(foo)

        def _provide_too_much_creation(self) -> GpsConsumerProvider:
            foo = self._create_foo()
            bar = Bar(foo)
            bar = Buz(foo) # violation, too many objects created in method
            baz = Baz(bar) # violation, too many objects created in method

            return GpsConsumerProvider(Baz)
    """

    results = linter.lint(class_node)

    assert results == [
        "invalid method name create_foo",
        "invalid method name bar",
        "invalid method name _bar",
        "invalid arguments in method name _provide_bad_bar_with_arg(self, badarg), should only receive self",
        "Logic found in _provide_some_logic, but is not permitted inside provider. found if foo:\n    pass. Solve this by moving logic outside of provider.",
        "Too many business objects are created in _provide_too_much_creation. This would create tight-coupling of object creation, which the provider aims to avoid",
    ]


def test_wrong_class_name():
    class_node = """
    class BadProviderSuffix:
        pass
    """

    results = linter.lint(class_node)

    assert results == ["Provider class names must end with the word Provider"]
