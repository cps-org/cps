History
=======

In the beginning, there was anarchy. Building a project which consumed a different, external project typically involved hand coding build directives based on assumptions where the external would be located.

Along came `pkg-config <https://www.freedesktop.org/wiki/Software/pkg-config/>`_. This was an improvement, but it was designed for UNIX-like platforms and isn't entirely portable. Also, while pkg-config does an adequate job describing the necessary compile and link flags to consume a package, this information is not always sufficient.

Some time later, CMake_ entered the scene, eventually gaining its own mechanism to describe a package. While this system solved many earlier problems, it relies on the CMake language and is therefore tightly coupled to that build system.

CPS attempts to solve these issues by taking the lessons learned by CMake and providing compatible information in a format that is not tied to the language of a particular build system.

What's wrong with pkg-config?
'''''''''''''''''''''''''''''

pkg-config was created way back in the bad old days of autotools, when everyone was using the same compiler and linker. It handles everything by direct specification of compile flags, which breaks down when multiple compilers with incompatible front-ends come into play and/or in the face of "superseded" features. (For instance, given a project consuming packages "A" and "B", requiring C++14 and C++11, respectively, pkg-config requires the build tool to translate compile flags back into features in order to know that the consumer should not be build with ``-std=c++14 ... -std=c++11``.)

Specification of link libraries via a combination of ``-L`` and ``-l`` flags is a problem, as it fails to ensure that consumers find the intended libraries. Not providing a full path to the library also places more work on the build tool (which must attempt to deduce full paths from the link flags) in order to compute appropriate dependencies in order to re-link targets when their link libraries have changed.

Last, pkg-config is not an ideal solution for large projects consisting of multiple components, as each component needs its own ``.pc`` file.

What's wrong with CMake exported targets?
'''''''''''''''''''''''''''''''''''''''''

CMake exported targets provide a richly featured mechanism for describing packages as a set of individual components, along with the necessary details for consuming each individual component. This generally works well... *for CMake*. The biggest problem with this system is not any internal flaw in the system, but the fact that it relies on the CMake language. Consumers have to parse not only CMake syntax, but in some cases need to cope with CMake generator expressions. Moreover, packages have access to the entire CMake language, which is Turing complete and capable of executing external processes. It would be exceptionally difficult for non-CMake tools to consume CMake package specifications without effectively reimplementing most or all of CMake itself. Clearly, this is not practical.

.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..

.. _CMake: https://cmake.org/

.. _P0235: http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0235r0.pdf

.. _WG21: http://www.open-std.org/jtc1/sc22/wg21/

.. kate: hl reStructuredText
