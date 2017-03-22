Usage and Implementation Recommendations
========================================

Single Package, Multiple Platforms
''''''''''''''''''''''''''''''''''

CPS intentionally does not directly provide for the possibility of a package that has multiple versions of components, built for different platforms. The recommended method for providing such a package is to provide a different ``.cps`` for each platform, such that the package bundle contains multiple ``.cps`` files. Components that are platform agnostic will appear in each ``.cps``. Proper use of platform-specific library directories will address the need for unique paths in most instances. On POSIX platforms, use of supplemental ``.cps`` files and symbolic or hard links may allow for a single file specifying platform-agnostic components to be shared.

Cross Compiling
'''''''''''''''

When cross compiling, it is sometimes necessary to consume parts of a package (e.g. a code generator) built for the host platform along with other parts of a package built for the target platform. As above, the CPS specification does not directly support a single package containing components for multiple platforms. In order to address this, it is recommended that tools (that support cross compiling) separately search for a package built for the host platform and a package built for the target platform, and select which instance's components to use as is appropriate to the situation.

When providing a package intended for cross-compiling use, keep in mind that the host-platform and target-platform packages do not need to contain the same components. Such a package might provide one ``.cps`` for the host platform containing only executables intended for compile-time use when building a consuming project, and a second ``.cps`` for the target platform that contains the libraries.

.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..

.. kate: hl reStructuredText
