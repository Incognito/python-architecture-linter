# Python Architecture Linter

Lint your python architecture, not just spacing.

# Example

```
poetry run python python_architecture_linter_cli/run.py /home/brian/target-project/

/runtime/provider.py:0  
    Node contains descendants which are not in the allow list  
    python_architecture_linter.ast_validators.nodeng_validator.validate_node_descendants_allow_list
```

# How it works

1. Define your architecture using a tree of Structure() instances
1. Add validators to validate a structure
1. Add node navigators to move to a deepr sub-structure
1. Run the command line from your project (for example, in a CI pipeline or in
   local development)


A structure is anything in your project that has some structure to it.
Typically projects follow this shape:

```
  ┌────────────────┐
  │                │
  │   Project      │
  │                │
  └───────┬────────┘
          │
          │
  ┌───────▼─────────┐
  │  Files          │
  │                 │
  │                 │
  └───────┬─────────┘
          │
          │
  ┌───────▼─────────┐
  │   Abstract      │
  │   Syntax Tree   │
  │                 │
  └─────────────────┘
```

You may wish your project definition to have a complex shape, typically to
support more features to to make defining rules simpler.  For example, instead
of one "every file" node in the tree, you may wish to have multiple types of
specific files which only get specific rules attached to them.

A validator runs against the structure, so if it is a file it is aware of the
file path, and contents. Projects are aware of the folder space. 

You must tell each structure how to navigate to its children based on type of
child. So if you have a file, something must read the file and parse the AST of
that file (note: this tooling is provided by this library already). If you wish
to add extra features on-top you need to add the instructions for
navigating from the parent structure to the child structure. 


# Package Structure
In-project applications should only depend on the definition of an architecture
and the runtime that they will use (for example, CLI). The definition could be
in your project or a stand-alone pypi package.

If you wish to extend usage beyond the core linter library and provide (as an
example) grimp support to validate imports over the project are working
intended you could add that logic to your own framework definition, or package
it up for re-use as a generic library that can be open-sourced (in wich case
you'd just consume it in your framework definition as if it were public).

This keeps releases minimal and prevents version conflicts. For example, if the
"core lib" shipped with grimp, it would force everyone to install it even if
using it indirectly. 

This is part of the philosophy of letting package consumers work their way out
of edge-cases without waiting for an upstream fix. They can just replace a tiny
component with a fork instead of replacing the entire library with a fork.

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





# Design Principles
1. Use generators to prevent the memory buildups that are common in other code
   quality tools and fail to work on average computers for on large projects,
or sometimes with large rulesets.
2. You can easily escape the limitations of the framework when you encounter an
   edgecase. If you need your own validators you should be able to do it
without rewriting a lot of unrelated code.
3. Project definitions are stand-alone projects.
4. Runtimes are stand-alone projects that consume a core.
