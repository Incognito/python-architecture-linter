# Python Architecture Linter

- Lint your python architecture, not just spacing.


# Design Principles

1. Use generators to prevent the memory buildups that are common in other code quality tools and fail to work on average computers for on large projects, or sometimes with large rulesets.
2. You can easily escape the limitations of the framework when you encounter an edgecase. If you need your own validators you should be able to do it without rewriting a lot of unrelated code.
3. Project definitions are stand-alone projects.
4. Runtimes are stand-alone projects that consume a core.
