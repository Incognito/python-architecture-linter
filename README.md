# Python Architecture Linter

Stability: Prototype. API may change without warning.

[![Python Architecture Linter](https://github.com/Incognito/python-architecture-linter/actions/workflows/main.yml/badge.svg)](https://github.com/Incognito/python-architecture-linter/actions/workflows/main.yml)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=python-architecture-linter&metric=coverage)](https://sonarcloud.io/dashboard?id=python-architecture-linter)
[![CodeFactor](https://www.codefactor.io/repository/github/incognito/python-architecture-linter/badge)](https://www.codefactor.io/repository/github/incognito/python-architecture-linter)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=python-architecture-linter&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=python-architecture-linter)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=python-architecture-linter&metric=security_rating)](https://sonarcloud.io/dashboard?id=python-architecture-linter)



Releases

- [![PyPI version fury.io](https://badge.fury.io/py/python-architecture-linter.svg)](https://pypi.python.org/pypi/python-architecture-linter/) python-architecture-linter
- [![PyPI version fury.io](https://badge.fury.io/py/python-architecture-linter-cli.svg)](https://pypi.python.org/pypi/python-architecture-linter-cli/) python-architecture-linter-cli
- [![PyPI version fury.io](https://badge.fury.io/py/python-architecture-linter-grimp-extension.svg)](https://pypi.python.org/pypi/python-architecture-linter-grimp-extension/) python-architecture-linter-grimp-extension
- [![PyPI version fury.io](https://badge.fury.io/py/modular-provider-architecture-definition.svg)](https://pypi.python.org/pypi/modular-provider-architecture-definition/) modular-provider-architecture-definition
- [![PyPI version fury.io](https://badge.fury.io/py/grimp_package_metrics.svg)](https://pypi.python.org/pypi/grimp-package-metrics/) grimp-package-metrics



Lint your architecture, not the syntax.

## What is an Architecture?
Architecture is not a tech stack or set of technologies you use in a project. For example, using
Django and Celery is not "an architecture". Architecture imposes design
constraints that enforces the structure of your code and data-flow in a
system. 

For example, Model-View-Controller is an architecture that constrains where you
put different kinds of code, and what code can call what other code. If your choice of MVC implies that Views cannot
*call* Models that is an architectural constraint on data-flow. If you decide
that Views cannot *import* from Models that is an additional leve of
constraint to enforce decoupling of code. You reasons for wanting these three different (but similar)
constraints are specific: 

- MVC itself gives you separation of concerns and better cohesion of your
  concepts.
- Call rules prevent unexpected data-flow in the system, which could simplify
  debugging or 
- Import rules can prevent tight-coupling of the system

All three rules can work together and make a project more maintainable, but
(depending on implementation needs) it could add "overhead work" because you
have to add extra code to satisfy the constraint. For example, instead of calling the database directly
from your templates you have to wire the model to the database call and route
it through the controller and inject the data to the view, and possibly re-map the database model to the view model too. These are trade-offs
in architecture choices which should be aligned with project design goals. If
you intend to hack a project together in a week and throw it away, maybe you
don't need those rules from above. Maybe those rules don't work in your
specific case. It might be that your needs actually change entirely over the
years and your architecture needs to change to reflect it. Often we find projects become unmaintainable because the architecture goals shifted slowly without anybody noticing or deliberately stating it.

Architecture is a reflection of the conventions a project follows, not what
tools it uses. Tools like Celery or Kafka both have their own architectures, but using them
in your project is just "an implementation detail" of an architecture (not the
architecture itself). Picking *how* you will use Celery or Kafka is an
"architecture convention". This becomes more obvious when we look at other
implementation details of projects like Redis or Postgres: you would never say "this
project has a Redis architecture", it sounds funny to say it because it is wrong. Some newer technologies like "AWS lambda" sound like "we use an AWS Lambda Architecture" but that tool itself is not the architecture, it doesn't define conventions, where code belongs, data-flow, or anything meaningful to help you build the system beyond "we use a PaaS solution".


## What is an Architecture Linter?

Architectures are expressions of a set of architecture conventions. Linters
validate a project against a set of rules. An Architecture Linter just focuses
on the Architecture of your project. This is in contrast to the traditional
jobs done with a Linter like `flake8` or `black`: checking for naming, spacing,
line-length, import sorting, etc.

There is some prior-work here, notably, `import-linter` which enforces import
direction rules in a project, and `pylint` which offers lots of code style
enforcement.

## What does python-architecture-linter do?

This project is a collection of python packages (maintained in one mono-repo)
which lets you define an arbitrary set of conventions (called an "architecture
definition"), and lint a project against those conventions.

You can package your architecture conventions as a pypi package, so they can be
versioned, added on to, bugfixed, and extended upon. The core of this library
is just tooling to crawl through an architecture definition and a target
project.

A working demo is available here:
https://github.com/Incognito/python-architecture-linter-demo/

In summary, this is the logical flow of work:

1. Define rules for an architecture
1. Write a project
1. Combine the rules and the project into the linter
1. Get a list of rule violation for that project

# Example output

```
poetry run python python_architecture_linter_cli/run.py /home/brian/target-project/

/runtime/provider.py:0
    Node contains descendants which are not in the allow list  
    python_architecture_linter.ast_validators.nodeng_validator.validate_node_descendants_allow_list
```


# How it works in more detail

Take a look inside `modular_provider_architecture_definition` for an example of
a definition. The README of that folder is the human-language expression of
everything the definition.py makes an attempt at enforcing.

### Step 1: Define your architecture using a tree of Structure() instances

Let's say you have a basic case, you want to enforce that there is a project
with more than one file, and all files must have file extensions.

```python
file = Structure("FILE")
project = Structure("PROJECT")
```

At the moment they do nothing and they are unaware of each-other.

### Step 2: Add validators to those "structures" in your project.

You need to create functions that validate the target structure and also return
a `python_architecture_linter.ValidationResult` with the status

You should have a specific data type in mind for every node. For example, you
may consider PROJECT to be a path to a project directory, and FILE to be just
one individual file (not a list of every file).

```python
import re
import glob

from python_architecture_linter import Structure, ValidationResult

def must_be_named_with_an_extension(file_path: str) -> ValidationResult:
    if re.search('\.[^\\.]*$', file_path):
	    return ValidationResult(
		explanation=f'No file extension found for {file_path}',
		is_valid=False,
		location=project_path,
		validator="must_be_named_with_an_extension",
	    )

    return ValidationResult(
        explanation="No issues found",
        is_valid=True,
        location=project_path,
        validator="must_have_more_than_one_file",
    )

def must_have_more_than_one_file(project_path: str) -> ValidationResult:
    if len(glob(project_path)) >=2:
	    return ValidationResult(
		explanation="Less than 2 files found",
		is_valid=False,
		location=project_path,
		validator="must_have_more_than_one_file",
	    )

    return ValidationResult(
        explanation="No issues found",
        is_valid=True,
        location=project_path,
        validator="must_have_more_than_one_file",
    )

file = Structure("FILE")
file.must([must_be_named_with_an_extension])

project = Structure("PROJECT")
project.must([must_have_more_than_one_file])
```

At first you might be annoyed that successful cases need to return an
explanation of why it passed, but this helps you in big complex projects when
you need to debug if a validator did or did not run, and why you received this
result. It also provides the advantage of not needing to inspect every return
type until you want to do something meaningful with them. Lastly, it lets you
keep a record of changes over time, so if a validator previously passed or
failed you can store those results and track them over time.


### Step 3: Define navigation between structures

We still only have two structures: FILE and PROJECT, but the relationship and
how to move between them is not coded. For this we need to describe what a structure "has" and the mapping of how to move from a parent-structure (eg, PROJECT) to a sub-structures (one specific FILE)


```python
import re
import glob

from python_architecture_linter import Structure, ValidationResult

def must_be_named_with_an_extension(file_path: str) -> ValidationResult:
    ...

def must_have_more_than_one_file(project_path: str) -> ValidationResult:
    ...

file = Structure("FILE")
file.must([must_be_named_with_an_extension])


# accepts the parent structure node type
# returns the sub-structure node type
def project_to_file(project_path: str) -> Iterable[File]: # always return an interable
    paths = Path(project_path).glob("**/*")

    # use of generators is preferred for memory reasons
    yield from paths

project = Structure("PROJECT", {
    "FILE": project_to_file  # show Project how to navigate into its own files
})
project.must([must_have_more_than_one_file])

project.has([file])  # Tell the project it has files
```


Now the `project` knows it `has` a `file` and it knows how to navigate into
this node. The way the API is structure here is a inelegant and likely to
change in the future.

Your project might "have" something else too, you could make custom filters to
jump directly to a dependency graph via `grimp` for example, or filter down to
just files in specific places or with specific names.

In my projects I will typically go from `project` to `specific_file` to
`specific_file_ast` and add rules to validate the code follows architecture
conventions.


### Step 4: 

The "root node" of your definition structure contains all rules inside it, so you can export it from your definition as something like `project_definition = project` and import it into the linter tooling. For example, if you want to directly use the CLI tooling and test your definition you can simple do this:

```python
from python_architecture_linter_cli import lint_command_factory

from your_local_project.definition import project_definition

lint_command = lint_command_factory(project_definition)
if __name__ == "__main__":
    lint_command()
```

You can then add it into your CI system or wherever you like. If you have more
complex needs the project was built with you in mind: you can bypass the CLI
entirely and write your own runtime to work against the core library. If you
want to expose a web API or store results in a database, you can.


# Package Structure

This repo is a "monorepo" which releases every folder as an individual pypi
package.

In-project applications should only depend on the `definition of an architecture`
and the `runtime` that they will use (for example, CLI). The structure
definition could be in your project or a stand-alone pypi package vendored to
you by some other project. You have all options open to you.

This small-specific-package style keeps releases minimal and prevents version
conflicts. For example, if the "core lib" shipped with new features that
brought extra heavy dependencies , it would force everyone to install it even
if using it indirectly. Instead, they get to opt-in to the parts they need
instead of "everything that we could ever imagine". This lets more users
actually use the tooling because they do not get superficial version conflicts
with parts of the software they do not actually need (for example, if the
linter needed some tiny bit of code in Django 3 but you were working on a
Django 2 project you could not use the tooling until after you upgraded, but it
might be that the tooling could help you solve architecture violations that
would let you upgrade sooner.

This is part of the philosophy of letting package consumers work their way out
of edge-cases without being blocked or waiting for an upstream fix. They can
just replace a tiny component with a fork instead of replacing the entire
library with a fork.

```
                           ┌──────────────────────┐
                           │ In-Project           ├────────────────┐
                           │    CI Scripts        │                │
                           └──────────┬───────────┘                │
                                      │                            │
                                      │                            │
                                      │                            │
┌────────────────────┐     ┌──────────▼───────────┐     ┌──────────▼──────────────────┐
│                    │     │  Framework           │     │ Python Architecture Linter  │
│  Grimp Extension   ◄─────┤  Definition          │     │   CLI                       │
│   SDK              │     │                      │     │                             │
└─────┬──────────┬───┘     └───────────────┬──────┘     └──────────┬──────────────────┘
      │          │                         │                       │
      │          │                         │                       │
      │          │                         │            ┌──────────▼──────────────────┐
      │          └─────────────────────────┴────────────►  Python Architecture Linter │
      │                                                 │   Core Lib                  │
      │                                                 └─────────────────────────────┘
 ┌────▼───────────┐
 │                │
 │   Grimp        │
 └────────────────┘
```


If you wish to extend usage beyond the core linter library and provide (as an
example) Machine Learning support to do something extra fancy, you have the
option of either adding that logic to your own structure definition, or package
it up for re-use as a generic library that can be open-sourced (in which case
you'd just consume it in your framework definition as if it were public). It
would be an "extension" to the core.



```
┌────────────────┐
│                │
│  ML Extension  │
│(you write this)│
└─────┬────── ───┘
      │          │    ┌─────────────────────────────┐
      │          └────►  Python Architecture Linter │
      │               │   Core Lib                  │
      │               └─────────────────────────────┘
 ┌────▼───────────┐
 │   ML Library   │
 │third party lib │
 └────────────────┘
```


# Design Principles
1. Use generators to prevent the memory buildups that are common in other code
   quality tools and fail to work on average computers for on large projects,
or sometimes with large rule-sets.
2. You can easily escape the limitations of the framework when you encounter an
   edge-case. If you need your own validators you should be able to do it
without rewriting a lot of unrelated code.
3. Project definitions are stand-alone projects.
4. Runtimes are stand-alone projects that consume a core.
