Usage and Implementation Recommendations
========================================

Configuration Use Cases
'''''''''''''''''''''''

First and foremost, package authors are **strongly recommended**
to set `configurations (package)`_
to a sensible list of default configurations
if their package provides multiple configurations.
This ensures that consumers
never fall back on unspecified behavior
when selecting a configuration.
The first default should be the configuration
that is most likely to be used by consumers
and/or is the most "safe" choice.
Additional, frequently used configurations
may be listed in priority order,
especially for packages where it would be reasonable
for the only available (installed) configuration
to be other than the first choice.

Recommended Use Cases
^^^^^^^^^^^^^^^^^^^^^

Because CPS configurations originated in CMake
and from the need to support CMake's existing usage,
it is natural that they support and expect similar use-cases.
In the context of CMake, configurations would typically be used
to select between possible build options,
but not between different configuration options.
While the line between these can be fuzzy,
a guideline we would recommend is that configurations
should select between *functionally compatible artifacts*.
The most typical usage in extant CMake projects |--|
selecting between builds with and without debug information,
or compiled at different optimization levels |--|
is an excellent example of a recommended use.

A similar suggested use is to select between builds
which have various levels of instrumentation enabled.
This might take the form of internal mechanisms,
or might encompass ABI-visible changes,
such as compiler-implemented "sanitization" functionality
("asan", "tsan", "ubsan", etc.).

Again, none of these use cases affect the *function* of an artifact.
This means that, in principle, a consumer's configuration selection
does not affect program behavior (aside from performance considerations).
In an ideal world, configurations would also be *ABI compatible*.
However, in practice, heterogeneous configuration selections
may result in incompatibilities.

At this time, the safest course of action
is to provide one or more configurations
which are ABI compatible with 'production-ready' artifacts.

Borderline Use Cases
^^^^^^^^^^^^^^^^^^^^

Without departing from our principle of functional interchangeability,
a library might offer internal differences
that do not affect its logical behavior,
such as providing multiple back-ends to accomplish the same task,
using different memory allocators internally,
or enabling parallel processing via OpenMP or GPU compute.
This seems like another good use case for configurations.
Another 'obvious' case is when offering both static and shared libraries.

A significant concern with these use cases, however,
is that they are likely to be orthogonal to,
and used in combination with,
the recommended "build style" use cases.
This shows that, in reality,
"configuration" is a combinatorial space
which is presently represented
only by a one-dimensional value.

At this time, we advise caution in choosing to use configurations
for the sorts of use cases described in this section.
While not impossible (see `Multi-Axis Configurations`_, below),
current tooling support is limited,
and problems may arise.

Non-Recommended Use Cases
^^^^^^^^^^^^^^^^^^^^^^^^^

Selecting Between Functionally Incompatible Libraries:
    As noted above, we advise using configurations
    only for selection of *functionally interchangeable* builds.
    Accordingly, we do *not* recommend using configurations
    to select between builds that provide different feature sets
    (for example, a network library with or without SSL support).

    Additionally, to the extent that consumers
    may need to be aware of such optional features
    when they do not otherwise affect the build interface,
    we recommend using symbolic components
    to communicate the availability of such optional features.

Selecting Between Semantically Incompatible Libraries:
    Use of configurations to select different components for linking
    is discouraged, both because of the combinatorial challenges,
    and because it makes it more difficult for consumers
    to understand what components are ultimately being linked.
    Additionally, selection of semantics
    (e.g. static vs. shared libraries)
    should typically be left to the user
    who is compiling the project and organizing the build environment,
    rather than being enforced by the consuming project.

Selecting Between Incompatible Platforms:
    Although platform compatibility is an area
    which is still very much under development in CPS,
    it is likely that compatibility will be expressed at the package level.
    Therefore, we do not recommend using configurations
    as a mechanism for platform selection.

Multi-Axis Configurations
'''''''''''''''''''''''''

Let's say your package includes
several configurations of a library,
where the configuration is logically specified
as a set of orthogonal attributes
(e.g. debug/release, static/shared).
How can this be exposed to consumers?

This is best accomplished via interface components.
For example:

.. code-block:: javascript

  "components": {
    "foo-static": {
      "type": "archive",
      "configurations": {
        "release": { ... },
        "debug": { ... }
      }, ...
    },
    "foo-shared": {
      "type": "dylib",
      "configurations": {
        "release": { ... },
        "debug": { ... }
      }, ...
    },
    "foo": {
      "type": "interface",
      "configurations": {
        "static": { "requires": [ ":foo-static" ] },
        "shared": { "requires": [ ":foo-shared" ] }
      }
    },
  },
  ...

This pattern allows the user
to specify their set of preferred configurations
like ``"static", "release"`` rather than ``"release_static"``.
When consuming the ``foo`` component,
the build tool will select on the static/shared axis,
which will bring in a component
whose configurations all match that choice.
The tool will then select the transitive component
on the remaining debug/release axis.
Longer chains can be constructed
to support configuration choices of arbitrary complexity.

Be aware, however, that tooling support for this method is limited.
In particular, existing tools may not support the *creation*
of artifacts with different configuration sets within a single build,
which makes the construction of such package descriptions problematic.
Additionally, while direct use may be practical,
indirect consumers of packages using such techniques
may run into issues.

It is hoped that the tooling ecosystem can improve in this respect,
however, at this time, anyone wishing to use such techniques
should be aware of the present limitations.
Nevertheless, it is recognized
that some projects, especially for legacy reasons,
may require the ability to allow consumers
to select from otherwise incompatible components
on the basis of configuration selection.

Single Package, Multiple Platforms
''''''''''''''''''''''''''''''''''

CPS intentionally does not directly
provide for the possibility of a package
that has multiple versions of components,
built for different platforms.
The recommended method for providing such a package
is to provide a different ``.cps`` for each platform,
such that the package bundle contains multiple ``.cps`` files.
Components that are platform agnostic
will appear in each ``.cps``.
Proper use of platform-specific library directories
will address the need for unique paths in most instances.
On POSIX platforms,
use of supplemental ``.cps`` files
and symbolic or hard links
may allow for a single file
specifying platform-agnostic components to be shared.

Cross Compiling
'''''''''''''''

When cross compiling, it is sometimes necessary
to consume parts of a package (e.g. a code generator)
built for the host platform
along with other parts of a package built for the target platform.
As above, the CPS specification does not directly support
a single package containing components for multiple platforms.
In order to address this, it is recommended that tools
(that support cross compiling)
separately search for a package
built for the host platform
and a package built for the target platform,
and select which instance's components to use
as is appropriate to the situation.

When providing a package intended for cross-compiling use,
keep in mind that the host-platform and target-platform packages
do not need to contain the same components.
Such a package might provide one ``.cps`` for the host platform
containing only executables intended for compile-time use
when building a consuming project,
and a second ``.cps`` for the target platform
that contains the libraries.

Link-Only Requirements and Link Order
'''''''''''''''''''''''''''''''''''''

In most cases, the order
in which "full" and link-only dependencies
are linked will not matter.
When an exception occurs,
it can be addressed in one of two manners:

- If a "full" dependency
  merely needs to be linked *after* a link-only dependency,
  the dependency can simply be listed twice;
  once in :attribute:`requires`,
  and again in :attribute:`link_requires`.
  (Tools are encouraged to add link-only dependencies
  after "full" dependencies.)
  This is redundant, but often satisfactory.

- If strict linking order without duplication is required,
  the link-only dependency may be wrapped
  in an :string:`"interface"` component
  which is listed as a "full" dependency.
  (Note that tools are expected to expand requirements
  depth-first rather than breadth-first.)

Transitive Dependencies
'''''''''''''''''''''''

When a package is located,
it is intended that the tool would also
locate any `requires (package)`_ mentioned by the package.
In some cases, however, a user may want to use
only some components of a package,
which may have a more limited set of dependencies
than the package as a whole
when every component of the package is considered.

It is plausible that a build tool
would take the package's requirements as advisory,
and only enforce those that are mentioned
by a component that the user has requested.
However, this does not account for dependencies
which apply only at run-time.
Additionally, since the intention is that a CPS file
originates from a compiled package,
and CPS provides mechanisms for the package to indicate
where its dependencies were located when the package was built,
it would be a strange situation that a package's requirements
should exist when the package is compiled,
but disappear before the package is used.
Even when obtaining a package via a distributor,
it is typical that installing the package
requires that the package's dependencies also be installed.

The obvious exception to this case
is when a package is split into multiple CPS files
at a functional-group level.
In this case, the CPS file for each group
should list the requirements applicable to that group.
Tools that support specifying
what components of a package must be provided
are permitted to ignore the information in any supplemental CPS file
that does not contribute requested components or configurations.
This allows the tool to accept a package
even if some of its requirements are not found,
if such requirements apply only to a functional-group
of the package that the user does not require.
(Even in this case, however, the usual case
would be that either the supplemental CPS file's requirements
can be satisfied anyway, for the reasons stated above,
or else the supplemental CPS file for such group
is not installed in the first place.)

.. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... ..

.. |--| unicode:: U+02014 .. em dash

.. kate: hl reStructuredText
