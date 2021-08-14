# Package quality metrics

You can tell a lot about a software system based on its import structure.

This project uses import graphs from `grimp` to provide various metrics to compute overall
quality of a system.

# Public API

Breaking the concept or interfaces here should be considered long-term stable.
If a replacement concept is introduced the previous functionality will be
marked deprecated but not broken until a new major version release.

## Package Quality Metrics

```
from grimp_package_metrics import get_all_package_metrics, PackageMetrics

results = get_all_package_metrics(grimp_graph)  # returns Iterator[PackageMetrics]

print(list(results))
```

### Why use this

https://en.wikipedia.org/wiki/Software_package_metrics

Get a quick idea at how likely changes to a package will cause "cascading
changes" to other parts of your system. If you push a number like "instability"
too-high you can be sure that future changes are probably going to make you
change many other parts of the system at once.

You also get to use it as a way
to tell when code is over-due for refactoring the "concrete details" out of the
"abstract machinery" that powers specific feature details.

More details about these numbers are commented in `grimp_package_metrics/coupling_metrics.py`

### Instability scores

Because module instability is hard to understand, here's a short explanation.
Instability by itself is not always something to fix, but rather just something
to be aware of.

Instability is a score that means you did something wrong, it instead helps you
identify what code belongs in what place.

In the below example (arrows always indicate dependency order), the Right-most module is unlikely (actually, with a score
of 0 it is impossible) to be broken by changes to the modules that score 1.0 If you break the interface, you need to rewrite every module that uses it, so the heavily-depended-on package should be small and abstract.

```
 ┌───┐
 │1.0├─────┐
 └───┘     │
 ┌───┐    ┌▼──┐
 │1.0├────►0.0│
 └───┘    └▲──┘
 ┌───┐     │
 │1.0├─────┘
 └───┘
```

You might have seen this structure before: multiple "plugins" depending on a "plugin interface". The concrete details are less stable than the abstraction, which means the details should have few dependencies and the interface should be "stable" and "unlikely to change" and also "unlikely to be broken" by something else.

The below example inverts the above example:

```
          ┌───┐
    ┌─────►0.0│
    │     └───┘
 ┌──┴┐    ┌───┐
 │1.0├────►0.0│
 └──┬┘    └───┘
    │     ┌───┐
    └─────►0.0│
          └───┘

```

This could be a good example of a facade which simplifies the interactions of 3
more complex subsystems. Changing a subsystem exposes the facade to breaking
changes. Depending on framework choices, this could also be how your
controllers look in an MVC application.

The next example demonstrates incoming and outgoing dependencies for a more complex system:
```
 ┌───┐             ┌───┐
 │1.0├─────┐ ┌─────►0.0│ 
 └───┘     │ │     └───┘
 ┌───┐    ┌▼─┴┐    ┌───┐
 │1.0├────►0.5├────►0.0│
 └───┘    └▲─┬┘    └───┘
 ┌───┐     │ │     ┌───┐
 │1.0├─────┘ └─────►0.0│
 └───┘             └───┘
```

In this case the central module is 0.5, meaning it is somewhere between
resilient and fragile when changed. It is possible that changing it is more
likely that a change to the system will break it than the 0.0 ranked modules.


### How to fix issues

Above you only saw instable packages depending on stable ones, but it is quite
common to have instability in the dependency graph: 

```

 ┌───┐             ┌───┐      ┌───┐
 │1.0├─────┐ ┌─────►0.0│   ┌──►0.0│
 └───┘     │ │     └───┘   │  └───┘
           │ │             │
 ┌───┐    ┌▼─┴┐    ┌────┐  │  ┌───┐
 │1.0├────►0.5├────►0.75├──┼──►0.0│
 └───┘    └▲─┬┘    └────┘  │  └───┘
           │ │             │
 ┌───┐     │ │     ┌───┐   │  ┌───┐
 │1.0├─────┘ └─────►0.0│   └──►0.0│
 └───┘             └───┘      └───┘
```

This is a problem because software maintainers are more likely to change the
0.75 module than 0.5, but the impact is often that a package must be
as-stable-as its highest ranked descendant, because the reasons to change code
that it depends on increases. You can fix this by breaking up the logic into
smaller modules, this reducing the overall likelihood that any one module can
cause cascading changes. You can also fix this by avoiding "proxying" or
"wrapping" another feature through one big package.

There is no ideal number for stability, but the ideal relationship is that
instable packages depend on more stable packages. As a side-effect, it means
the most stable packages do not contain details relevant to frequent change.
Usually this takes the form of interfaces or libraries. Take care to not think
an abstract or "generic library" means it covers every use case. You know it is more
abstract when there are fewer business details (reasons to change) inside of it.


## Dependency Cycle Detection

```
from grimp_package_metrics import dependency_cycles

results = list(dependency_cycles(grimp_graph))  # returns Iterator[List[str]]

print(list(results))
```

### Why use this

A cycle in dependencies looks like this:

```
 ┌───┐    ┌───┐
 │ A ├────► B │
 └─▲─┘    └─┬─┘
   │  ┌───┐ │
   └──┤ C ◄─┘
      └───┘
```

It means that any change to module A might need changes from C, and C might
need changes from B, and B might need changes from A. In general this design
ensures that when you change one line of code that is inside a cycle you must
consider the entire system of A-B-C to make any change. You lose all isolation and the programmer must consider the full complexity of the change.

Consider this alternative which makes `A->C` (previously it was `C->A`)):

```
 ┌───┐    ┌───┐
 │ A ├────► B │
 └─┬─┘    └─┬─┘
   │  ┌───┐ │
   └──► C ◄─┘
      └───┘
```

With this design your changes are limited to how far they can spiral into other
systems. Changes to A can be considered without needing to change B. Even
better, you can change C with only considering how changes will impact "A and
B, and how B is used by A" but not "how C is used by B which is used by A which
is used by C which is used by B...". You can escape the cognitive infinite loop
which causes engineers to spend hours debugging minor changes.

In summary: if you have many packages in a loop, you must treat them as one big
package, it's better to do that or find a way to repair the dependency chain.

### How to fix this

Often the fix is one of two simple options:

Option one: Often the actual dependency is something that operates as an interface or a data contract. Move it to its own package and make both packages depend on it instead.

```
 ┌──┐   ┌──┐
 │A ├───►B │
 └─┬┘   └─┬┘
   │      │
 ┌─▼┐   ┌─▼┐
 │Ai◄───┤C │ # Ai is the common interface A and C needed.
 └──┘   └──┘
```

Option two:

Your runtime logic is organised in the wrong place, you force an unrelated
module (A) to organise how two other modules (B and C) do their work. In this
case you can simply move the logic into B by finding the right design patterns
to handle the logic.

```
 ┌──┐   ┌──┐
 │A ├───►B │
 └──┘   └─┬┘
          │
        ┌─▼┐
        │C │ # A never needed to depend on C
        └──┘ # logic was moved into B
```
