# Modular provider architecture

This package defines an opinionated architecture that is:

- **Modular** 
- Uses **"instance providers"** 
- Exposes conventions for a **Runtime**

## Modular

Modularity brings some benefits. You can modify, remove or replace a software
component without spiraling changes across the entire project. You can re-use
components in ways that were never before considered.

For example, if you define a module for a Postgres database connection, your project
should be able to connect to 50 different databases using the same code.
Secondly, your project should be able to also add a MongoDB component which can
also let your application connect to hundreds of databases at the same time.

This is easier said than done and requires decoupling from other components in
the software and only letting dependencies (eg, `import` statements) be formed
when there is a concrete logical need (instead of a convenience short-cut when
writing code).

You should be able to select the folder for a software component and run a `git
subtree-split` to extract it into its own stand-alone software package (with
minor work to add a new dependency file and adjust import names).


It means you have a tree structure like this:

```
    modular_provider_architecture
    ├── __init__.py
    ├── logic_module
    │   ├── __init__.py
    │   ├── logic.py
    │   └── provider.py
    └── module_runtime
        ├── __init__.py
        ├── provider.py
        ├── run.py
        └── runtime.py
```

Every top-level folder is a "module" in this architecture. This language may be
confusing in python so feel free to call it a component instead if that's less
confusing for your team.

The concept of a "submodule" is a violation of this architecture as it forces
heavily coupling between components. Keep it all on one folder level, and pick
good names. If you have too many folders it is a good indication that your
project has grown too large, and development would be easier if you created two
projects with 1 common package made from common software components (remember,
you can use `git subtree-split` to move code around to a new home and keep the
history)

Your software dependencies should look one-way:

```
 ┌────────────┐
 │ module     │
 │  _runtime  │
 └─────┬──────┘
       │
       │Depends on
       │ ("imports from")
       │
       │
       ▼
       ▼
 ┌─────▼──────┐
 │ logic      │
 │  _module   │
 └────────────┘
```

If you have any "cycles" in your architecture it is likely that you need to
make a simple package in-between to keep the common information (often this is
just an interface or some similar data)

In this architecture there are two major types of object instances:

1. "Infrastructure", it moves data around and processes it
2. "Data Transfer Objects" which represent state.

You can only create infrastructure inside a "Provider". We don't create new
classes "on-the-fly" inside DTOs or other infrastructure.

## Instance Providers

The instance provider is here to help you keep code decoupled so you can re-use
it in ways you never expected.

If you used an IoC container this will feel familiar to you, the only
difference is it is done without any third-party library.

```python
from some_module.internals import UsefulClass, Details

class SomeModuleProvider:
    def provide_instance_for_other_modules(self)
        """
	By naming convention, "instance_for_other_modules" is the "name" of
	these instances, they not accept any parameters to modify values
        because they become "unnamed" if that happens, (you don't know what it will
        return). That can be done with _create methods.
        """
        details_for_useful_class = self._provide_instance_privately_to_this_provider()
        return UsefulClass(details_for_useful_class)

    def _provide_instance_privately_to_this_provider(self)
        """
	Same as above, except you don't want anyone to use these externally.
        They're private.
        """
        return Details("Private")

    def _create_code_duplicated_often(self, modifier1, modifier2)
        """
	Useful when you want to avoid duplcating code freqnetly to change some
	details. Concrete instances still need to go through a provider
        however. Public crete methods are not allowed.
        """
        return Details(modifier1 + modifier2)
```

If you wish to return a single-instance for a method that is called many times,
use of the `functools.cache` decorator is an easy way to get a "singleton" on
the instance of a provider without enforcing it on every software component
that uses this provider.


The above code would look like this if we were using `python-dependency-injector` instead:

```python
from dependency_injector import containers, providers
from some_module.internals import UsefulClass, Details

def _create_code_duplicated_often(self, modifier1, modifier2)
    return Details(modifier1 + modifier2)

class Container(containers.DeclarativeContainer):
    _detail_provider = providers.Factory(Details)
    useful_class_provider = providers.Object(UsefulClass, _detail_provider)
```

We don't permit logic inside providers, they are strictly there to orchestrate
how "infrastructure" is put together. Detecting if "the environment is dev" is
also not permitted anywhere and generally a bad practice.

Using a provider is only permitted in other providers or in `run.py` file.

The provider structure is intentionally designed to provide a new instance by
default instead of re-use instances (re-use is instead an opt-in behaviour).
This means when you have two or three run.py files in a project you can
deterministically map out where side-effects come from, but also you introduce
"bulkheads" against side-effects from other instances. Breaking the database
connection used by one component doesn't need to break the database connections
for everything else in your application unless you specifically want it to.

This also has advantages for threaded applications as you now have fine-grained
control over what instances are shared and which ones are re-created in
threads.

The downside is that the overall memory footprint might be a bit larger.
Because we're mostly talking about "infrastructure" you should expect the
memory footprint to not grow with data processed through the application but
rather how often a provider is used by another module. If you have a common
component used 10 times it will create 10 instances. This is manageable however
as the memory footprint of your infrastructure will be deterministic and
measurable the moment you "run" your application, you do not need to test it
with different workloads, everything is provisioned in memory once the
application starts. This also means the difference between memory footprint at
any point at runtime and the size when the application started is equal to the
amount of "data state" being held in the system.


## Runtime

Runtimes are minimal. They should be the absolute smallest amount of code to
plug in your main application to some kind of runtime environment.

Your runtime might be a command-line, http-daemon, queue consumer, background
cron job runner, or anything else that "starts" your program.

You should always define a `run.py` in the root level of a runtime component
and expect that this is where your software will be started.


