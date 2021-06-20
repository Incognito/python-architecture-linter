from modular_provider_architecture.runtime_module.provider import RuntimeProvider

if __name__ == "__main__":
    provider = RuntimeProvider()
    runtime = provider.provide_runtime()
    runtime.run()
