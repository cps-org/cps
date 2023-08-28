Usage and Implementation Recommendations
========================================

Configurations as Flags
'''''''''''''''''''''''

Let's say your package includes
several configurations of a library,
where the configuration is logically specified
as a set of orthogonal attributes
(e.g. debug/release, static/shared).
What's the best way to provide these to your users?

This is best accomplished via interface components.
For example:

.. code-block:: javascript

  "Components": {
    "foo-static": {
      "Type": "archive",
      "Configurations": {
        "Release": { ... },
        "Debug": { ... }
      }, ...
    },
    "foo-shared": {
      "Type": "dylib",
      "Configurations": {
        "Release": { ... },
        "Debug": { ... }
      }, ...
    },
    "foo": {
      "Type": "interface",
      "Configurations": {
        "Static": { "Requires": [ "foo-static" ] },
        "Shared": { "Requires": [ "foo-shared" ] }
      }
    },
  },
  ...

This pattern allows the user
to specify their set of preferred configurations
like ``"Static", "Release"`` rather than ``"ReleaseStatic"``.
When consuming the ``foo`` component,
the build tool will select on the static/shared axis,
which will bring in a component
whose configurations all match that choice.
The tool will then select the transitive component
on the remaining debug/release axis.
Longer chains can be constructed
to support configuration choices of arbitrary complexity.
Where appropriate
(and assuming that the package does not wish to support
the user naming the "real" components directly),
the component graph can be constructed in a way
that allows shared attributes
to be specified at the higher level interface components.

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
  once in :attribute:`Requires`,
  and again in :attribute:`Link-Requires`.
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
locate any `Requires (Package)`_ mentioned by the package.
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

.. kate: hl reStructuredText
