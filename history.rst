History
=======

In the beginning, there was anarchy.
Building a project which consumed a different, external project
typically involved hand coding build directives
based on assumptions where the external would be located.

The first attempts to tame this mess were disorganized,
with hundreds of projects
each developing their own bespoke mechanisms
for managing dependencies
and making themselves available
to further dependents in turn.
One approach that saw wider adoption
was to provide a script or micro-application
which described the capabilities and usage directives of a project.
These "config" tools, when queried,
provided the necessary compile and link flags
to build against a given library.
(As of 2024, some projects
continue to ship such tools,
though often in conjunction
with other, more modern alternatives.)

GNOME dreamed of a single package configuration script to rule them all,
providing all the necessary flags from a single pseudo-database.
Entries in the database would be distributed alongside their libraries,
which would no longer have to maintain their own utilities.
This dream first arrived as gnome-config,
which encompassed all the libraries in the GNOME project,
but would not be enough.
This was followed by the venerable `pkg-config`_,
which could encompass all the libraries in the world,
and is still in use over two decades later.

Meanwhile, CMake_, making its own foray
into this untamed wilderness at almost the same time,
was faced with the problem that many packages
came with only a library and header files.
(This was especially true on Windows,
which lacked autotools,
and even cross-platform projects
often treated Windows as an afterthought at best.)
Needing an immediate solution,
CMake could not rely on information
shipped alongside libraries,
so it provided a library of built-in "find modules"
to cover many common dependencies.
Although augmented by the ability
for consumers to write and ship their own find modules
for packages not included in the CMake distribution,
this resulted in developers working independent of each other
writing multiple versions of such modules
that were often incompatible with each other
(or with "first party" modules
which sometimes became available as time progressed).

Cataloging all the world's software was not practical,
and the superiority of each package describing itself was evident
(in this respect, pkg-config had the right idea).
This spreads the workload and ensures consistency.
To this end, CMake created its own means for projects to "export"
their own descriptions of their usage requirements.
Compared to pkg-config, these descriptions
provided much more information about the libraries themselves,
allowing CMake to derive the appropriate compile and link arguments
rather than hoping that the pre-computed arguments are adequate.
This represented a significant advancement
in the state of package information exchange,
although it retains its own limitations.

While pkg-config does an adequate job
describing the necessary compile and link flags to consume a component,
its approach is suboptimal for describing related but separable consumables,
and `flag soup`_ is semantically lossy and not always sufficient (see below).
CMake's most recent system solves many problems,
but relies on the CMake language
and is therefore tightly coupled to that build system.

CPS attempts to solve these issues
by taking the lessons learned by CMake
and providing compatible information in a format
that is not tied to the language of a particular build system.

What's wrong with pkg-config?
'''''''''''''''''''''''''''''

Although pkg-config was a huge step forward
in comparison to the chaos that had reigned previously,
it retains a number of limitations.
For one, it targets UNIX-like platforms
and is somewhat reliant on the |FHS|_.
Also, it was created at a time when autotools reigned supreme
and, more particularly, when it could reasonably be assumed
that everyone was using the same compiler and linker.
It handles everything by direct specification of compile flags,
which breaks down when multiple compilers
with incompatible front-ends come into play
and/or in the face of "superseded" features.
(For instance, given a project consuming packages "A" and "B",
requiring C++14 and C++11, respectively,
pkg-config requires the build tool
to translate compile flags back into features
in order to know that the consumer
should not be built with ``-std=c++14 ... -std=c++11``.)

Specification of link libraries
via a combination of ``-L`` and ``-l`` flags is a problem,
as it fails to ensure that consumers find the intended libraries.
Not providing a full path to the library
also places more work on the build tool
(which must attempt to deduce full paths from the link flags)
to compute appropriate dependencies
in order to re-link targets when their link libraries have changed.

Last, pkg-config is not an ideal solution
for large projects consisting of multiple components,
as each component needs its own ``.pc`` file.

What's wrong with CMake exported targets?
'''''''''''''''''''''''''''''''''''''''''

CMake exported targets provide a richly featured mechanism
for describing packages as a set of individual components,
along with the necessary details for consuming each individual component.
This generally works well... *for CMake*.

Even so, it is not perfect.
Version compatibility management remains partly bespoke,
and official support for transitive dependencies
is only partially implemented as of CMake 3.30.

However, the biggest problem by far
is not any internal flaw in the system,
but the fact that it relies on the CMake language.
Consumers have to parse not only CMake syntax,
but in some cases need to cope with CMake generator expressions.
Moreover, packages have access to the entire CMake language,
which is Turing complete and capable of executing external processes.
It would be exceptionally difficult for non-CMake tools
to consume CMake package specifications
without effectively reimplementing most or all of CMake itself.
Clearly, this is not practical.

Even so, certain tasks that should be easy,
such as handling transitive dependencies
or specifying version compatibility,
are difficult and may require hand-writing code.
While there is plenty of room for improvement
without leaving the CMake ecosystem,
CPS offers similar room for growth
while also opening up package distribution
to a wider audience of consumers.

.. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... ..

.. _pkg-config: https://www.freedesktop.org/wiki/Software/pkg-config/

.. _CMake: https://cmake.org/

.. _flag soup: https://wg21.link/p2800

.. _FHS: https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard

.. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... ..

.. |FHS| replace:: Filesystem Hierarchy Standard

.. kate: hl reStructuredText
