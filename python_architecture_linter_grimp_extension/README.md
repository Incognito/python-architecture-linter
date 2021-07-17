Plugs grimp into python-architecture-linter

# Public API:

tbd

# Anticipated usage

```python
# your project definition.py

from python_architecture_linter.node_navigators import project_to_files
from python_architecture_linter_grimp_extension.grimp_navigators import (
    files_to_import_statements,
    import_statements_to_graph,
)
from python_architecture_linter import Structure


import_graph = Structure("IMPORT_GRAPH", {})
import_graph.must([]) # add validators here


import_statements = Structure("IMPORT_STATEMENTS", {"IMPORT_GRAPH": import_statements_to_graph})
import_statements.has([import_graph])
project_files = Structure("ALL_PATHON_FILES", {"IMPORT_STATEMENTS": files_to_import_statements})
project_files.has([import_statements])
project = Structure("PROJECT", {"ALL_PATHON_FILES": project_to_files})
project.has([project_files])
```

# Example validators


You should be able to port logic from projects that work with `grimp` graphs (eg, `import-linter` Contracts) quite easily:

```python
def must_not_import_bar_into_foo(graph):
    forbidden_import_details = graph.get_import_details(
        importer="foo",
        imported="bar"
    )
    import_exists = bool(forbidden_import_details)

    return ContractCheck(
        kept=not import_exists,
        metadata={
    	'forbidden_import_details': forbidden_import_details,
        }
    )

```

You will likely want to curry different constraints into the validator or bake them into a class with a pre-linting step, eg:

```
importer="foo"
imported="bar"
must_not_import_bar_into_foo = must_not_import(importer, imported) # just a simple factory that returns the `must_` validator

import_graph = Structure("IMPORT_GRAPH", {})
import_graph.must([must_not_import_bar_into_foo]) # add validators here
```


# Project

The project is maintained in a monorepo at https://github.com/Incognito/python-architecture-linter
