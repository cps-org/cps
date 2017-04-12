Package Schema
==============

Objects
'''''''

:object:`Package`\ :hidden:`(Object)`
-------------------------------------

The root of a CPS document is a |package| object. A |package| object describes a single package.

:object:`Platform`\ :hidden:`(Object)`
--------------------------------------

A |platform| describes the platform on which a package's components may run.

:object:`Requirement`\ :hidden:`(Object)`
-----------------------------------------

A |requirement| describes the specifics of a package dependency.

:object:`Component`\ :hidden:`(Object)`
---------------------------------------

A |component| is a consumable part of a package. Typical components include libraries and executables.

:object:`Configuration`\ :hidden:`(Object)`
-------------------------------------------

A |configuration| holds attributes that are specific to a particular configuration of a |component|.

Attributes
''''''''''

An optional attribute may have the value |null|. This shall be equivalent to omitting the attribute.

Attribute names are case insensitive, although it is recommended that ``.cps`` files use the capitalization as shown.

:attribute:`C-Runtime-Vendor`
-----------------------------

:Type: |string|
:Applies To: |platform|
:Required: No

Specifies that the package's CABI components require the specified C standard/runtime library. Typical (case-insensitive) values include :string:`"bsd"` (libc), :string:`"gnu"` (glibc), :string:`"mingw"` and :string:`"microsoft"`.

:attribute:`C-Runtime-Version`
------------------------------

:Type: |string|
:Applies To: |platform|
:Required: No

Specifies the minimum C standard/runtime library version required by the package's CABI components.

:attribute:`Clr-Vendor`
-----------------------

:Type: |string|
:Applies To: |platform|
:Required: No

Specifies that the package's CLR (.NET) components require the specified `Common Language Runtime`_ vendor. Typical (case-insensitive) values include :string:`"microsoft"` and :string:`"mono"`.

:attribute:`Clr-Version`
------------------------

:Type: |string|
:Applies To: |platform|
:Required: No

Specifies the minimum `Common Language Runtime`_ version required to use the package's CLR (.NET) components.

:attribute:`Compat-Version`
---------------------------

:Type: |string|
:Applies To: |package|
:Required: No

Specifies the oldest version of the package with which this version is compatible. This information is used when a consumer requests a specific version. If the version requested is equal to or newer than the :attribute:`Compat-Version`, the package may be used.

If not specified, the package is not compatible with previous versions (i.e. :attribute:`Compat-Version` is implicitly equal to :attribute:`Version`).

:attribute:`Compile-Features`
-----------------------------

:Type: |string-list|
:Applies To: |component|, |configuration|
:Required: No

Specifies a list of `Compiler Features`_ that must be enabled or disabled when compiling code that consumes the component.

:attribute:`Compile-Flags`
--------------------------

:Type: |language-string-list|
:Applies To: |component|, |configuration|
:Required: No

Specifies a list of additional flags that must be supplied to the compiler when compiling code that consumes the component. Note that compiler flags may not be portable; use of this attribute is discouraged.

A map may be used instead to give different values depending on the language of the consuming source file. Handling of such shall be the same as for `Definitions`_.

:attribute:`Components` :applies-to:`(Package)`
-----------------------------------------------

:Type: |map| to |component|
:Applies To: |package|
:Required: Yes

Specifies the components which the package provides. Keys are the component names.

:attribute:`Components` :applies-to:`(Requirement)`
---------------------------------------------------

:Type: |string-list|
:Applies To: |requirement|
:Required: No

Specifies a list of components which must be present in the required package in order for the requirement to be satisfied. Although the build tool will generally produce an error if a consumer uses a component which in turn requires a component that was not found, early specification via this attribute may help build tools to diagnose such issues earlier and/or produce better diagnostics.

:attribute:`Configuration`
--------------------------

:Type: |string|
:Applies To: |package|
:Required: Special

Specifies the name of the configuration described by a configuration-specific ``.cps`` (see `Configuration Merging`_). This attribute is required in a configuration-specific ``.cps``, and ignored otherwise.

:attribute:`Configurations` :applies-to:`(Package)`
---------------------------------------------------

:Type: |string-list|
:Applies To: |package|
:Required: No

Specifies the configurations that are available. See `Package Configurations`_ for a description of how configurations are used.

:attribute:`Configurations` :applies-to:`(Component)`
-----------------------------------------------------

:Type: |map| to |configuration|
:Applies To: |component|
:Required: No

Specifies a set of configuration-specific attributes for a |component|. Keys are the configuration names.

:attribute:`Cpp-Runtime-Vendor`
-------------------------------

:Type: |string|
:Applies To: |platform|
:Required: No

Specifies that the package's CABI components require the specified C standard/runtime library. Typical (case-insensitive) values include :string:`"gnu"` (libstdc++), :string:`"llvm"` (libc++) and :string:`"microsoft"`.

:attribute:`Cpp-Runtime-Version`
--------------------------------

:Type: |string|
:Applies To: |platform|
:Required: No

Specifies the minimum C standard/runtime library version required by the package's CABI components.

:attribute:`Cps-Path`
---------------------

:Type: |string|
:Applies To: |package|
:Required: No

Specifies the directory portion location of the ``.cps`` file. This shall be an "absolute" path which starts with ``@prefix@``. This provides an additional mechanism by which the tool may deduce the package's prefix, since the absolute location of the ``.cps`` file will be known by the tool. (See also `Prefix Determination`_.)

:attribute:`Cps-Version`
------------------------

:Type: |string|
:Applies To: |package|
:Required: No

Specifies the version of the CPS to which this ``.cps`` file conforms. This may be used by tools to provide backwards compatibility in case of compatibility-breaking changes in the CPS. If not specified, behavior is implementation defined.

:attribute:`Default-Components`
-------------------------------

:Type: |string-list|
:Applies To: |package|
:Required: No

Specifies a list of components that should be inferred if a consumer specifies a dependency on a package, but not a specific component.

:attribute:`Definitions`
------------------------

:Type: |language-string-list|
:Applies To: |component|, |configuration|
:Required: No

Specifies a list of compile definitions that must be defined when compiling code that consumes the component. Definitions should be in the form :string:`"FOO"` or :string:`"FOO=BAR"`. Additionally, a definition in the form :string:`"!FOO"` indicates that the specified symbol (``FOO``, in this example) shall be explicitly undefined (e.g. ``-UFOO`` passed to the compiler).

A map may be used instead to give different values depending on the language of the consuming source file. In this case, the build tool shall select the list from the map whose key matches the (case-insensitive) language of the source file being compiled. Recognized languages shall include :string:`"C"`, :string:`"C++"`, and :string:`"Fortran"`.

:attribute:`Hints`
------------------

:Type: |string-list|
:Applies To: |requirement|
:Required: No

Specifies a list of paths where a required dependency might be located. When given, this will usually provide the location of the dependency as it was consumed by the package when the package was built, so that consumers can easily find (correct) dependencies if they are in a location that is not searched by default.

:attribute:`Includes`
---------------------

:Type: |language-string-list|
:Applies To: |component|, |configuration|
:Required: No

Specifies a list of directories which should be added to the include search path when compiling code that consumes the component. If a path starts with ``@prefix@``, the package's install prefix is substituted (see `Package Searching`_). This is recommended, as it allows packages to be relocatable.

A map may be used instead to give different values depending on the language of the consuming source file. Handling of such shall be the same as for `Definitions`_.

:attribute:`Isa`
----------------

:Type: |string|
:Applies To: |platform|
:Required: No

Specifies that the package's CABI components require the specified `Instruction Set Architecture`_. The value is case insensitive and should follow the output of ``uname -m``.

:attribute:`Jvm-Vendor`
-----------------------

:Type: |string|
:Applies To: |platform|
:Required: No

Specifies that the package's Java components require the specified Java_ vendor. Typical (case-insensitive) values include :string:`"oracle"` and :string:`"openjdk"`.

:attribute:`Jvm-Version`
------------------------

:Type: |string|
:Applies To: |platform|
:Required: No

Specifies the minimum Java_ Virtual Machine version required to use the package's Java components.

:attribute:`Kernel`
-------------------

:Type: |string|
:Applies To: |platform|
:Required: No

Specifies the name of the operating system kernel required by the package's components. The value is case insensitive and should follow the output of ``uname -s``. Typical values include :string:`"windows"`, :string:`"cygwin"`, :string:`"linux"` and :string:`"darwin"`.

:attribute:`Kernel-Version`
---------------------------

:Type: |string|
:Applies To: |platform|
:Required: No

Specifies the minimum operating system kernel version required by the package's components.

:attribute:`Link-Features`
--------------------------

:Type: |string-list|
:Applies To: |component|, |configuration|
:Required: No

Specifies a list of `Linker Features`_ that must be enabled or disabled when compiling code that consumes the component.

:attribute:`Link-Flags`
-----------------------

:Type: |string-list|
:Applies To: |component|, |configuration|
:Required: No

Specifies a list of additional flags that must be supplied to the linker when linking code that consumes the component. Note that linker flags may not be portable; use of this attribute is discouraged.

:attribute:`Link-Languages`
---------------------------

:Type: |string-list|
:Applies To: |component|, |configuration|
:Required: No

Specifies the ABI language or languages of a static library (`Type`_ :string:`"archive"`). Officially supported (case-insensitive) values are :string:`"C"` (no special handling required) and :string:`"C++"` (consuming the static library also requires linking against the C++ standard runtime). The default is :string:`"C"`.

:attribute:`Link-Libraries`
---------------------------

:Type: |string-list|
:Applies To: |component|, |configuration|
:Required: No

Specifies a list of additional libraries that must be linked against when linking code that consumes the component. (Note that packages should avoid using this attribute if at all possible. Use `Requires (Component)`_ instead whenever possible.)

:attribute:`Link-Location`
--------------------------

:Type: |string|
:Applies To: |component|, |configuration|
:Required: No

Specifies an alternate location of the component that should be used when linking against the component. This attribute typically applies only to :string:`"dylib"` components on platforms where the library is separated into multiple file components. For example, on Windows, this attribute shall give the location of the ``.lib``, while `Location`_ shall give the location of the ``.dll``.

If the path starts with ``@prefix@``, the package's install prefix is substituted (see `Package Searching`_). This is recommended, as it allows packages to be relocatable.

:attribute:`Link-Requires`
--------------------------

:Type: |string-list|
:Applies To: |component|, |configuration|
:Required: No

Specifies additional components required by a component which are needed only at the link stage. Unlike `Requires (Component)`_, only the required components' link dependencies should be applied transitively; additional properties such as compile and include attributes of the required component(s) should be ignored.

:attribute:`Location`
---------------------

:Type: |string|
:Applies To: |component|, |configuration|
:Required: Depends

Specifies the location of the component. The exact meaning of this attribute depends on the component type, but typically it provides the path to the component's primary artifact, such as a ``.so`` or ``.jar``. (For Windows DLL components, this should be the location of the ``.dll``. See also `Link-Location`_.)

If the path starts with ``@prefix@``, the package's install prefix is substituted (see `Package Searching`_). This is recommended, as it allows packages to be relocatable.

This attribute is required for |component|\ s that are not of :string:`"interface"` :attribute:`Type`.

:attribute:`Name`
-----------------

:Type: |string|
:Applies To: |package|
:Required: Yes

Specifies the canonical name of the package. In order for searching to succeed, this must exactly match the name of the CPS file without the ``.cps`` suffix.

:attribute:`Platform`
---------------------

:Type: |platform|
:Applies To: |package|
:Required: No

Specifies the platform on which a package's components may run. This allows tools to ignore packages which target a different platform than the platform that the consumer targets (see `Package Searching`_). Any platform attribute not specified implies that the package's components are agnostic to that platform attribute. If this attribute is not specified, the package is implied to be platform agnostic. (This might be the case for a "library" which consists entirely of C/C++ headers. Note that JVM/CLR versions are platform attributes, so packages consisting entirely of Java and/or CLR components will still typically use this attribute.)

:attribute:`Requires` :applies-to:`(Component)`
-----------------------------------------------

:Type: |string-list|
:Applies To: |component|, |configuration|
:Required: No

Specifies additional components required by a component. This is used, for example, to indicate transitive dependencies. Relative component names are interpreted relative to the current package. Absolute component names must refer to a package required by this package (see `Requires (Package)`_). Compile and link attributes should be applied transitively, as if the consuming component also directly consumed the components required by the component being consumed.

See also `Link-Requires`_.

:attribute:`Requires` :applies-to:`(Package)`
---------------------------------------------

:Type: |map| to |requirement|
:Applies To: |package|
:Required: No

Specifies additional packages that are required by this package. Keys are the name of another required package. Values are a valid |requirement| object or |null| (equivalent to an empty |requirement| object) describing the package required.

:attribute:`Type`
-----------------

:Type: |string| (restricted)
:Applies To: |component|
:Required: Yes

Specifies the type of a component. The component type affects how the component may be used. Officially supported values are :string:`"archive"` (CABI static library), :string:`"dylib"` (CABI shared library), :string:`"module"` (CABI plugin library), :string:`"jar"` (Java Archive), and :string:`"interface"`. If the type is not recognized by the parser, the component shall be ignored. (Parsers are permitted to support additional types as a conforming extension.)

A :string:`"dylib"` is meant to be linked at compile time; the :attribute:`Location` specifies the artifact required for such linking (i.e. the import library on PE platforms). A :string:`"module"` is meant to be loaded at run time with :code:`dlopen` or similar; again, the :attribute:`Location` specifies the appropriate artifact.

An :string:`"interface"` component is a special case; it may have the usual attributes of a component, but does not have a location. This can be used to create "virtual" components that do not have an associated artifact.

:attribute:`Version` :applies-to:`(Package)`
--------------------------------------------

:Type: |string|
:Applies To: |package|
:Required: No

Specifies the version of the package. Although there is no restriction on the format of the version text, successful version matching may impose restrictions.

If not provided, the CPS will not satisfy any request for a specific version of the package.

:attribute:`Version` :applies-to:`(Requirement)`
------------------------------------------------

:Type: |string|
:Applies To: |requirement|
:Required: No

Specifies the required version of a package. If omitted, any version of the required package is acceptable. Semantics are the same as for the :attribute:`Version` attribute of a |package|.

Notes
'''''

- Unless otherwise specified, a relative file path appearing in a CPS shall be interpreted relative to the ``.cps`` file.

- Unless otherwise specified, unrecognized attributes shall be ignored. This makes it easier for tools to add tool-specific extensions. (It is *strongly* recommended that the names of any such attributes start with ``X-<tool>-`` (where ``<tool>`` is the name of the tool which introduced the extension) in order to reduce the chance of conflicts with newer versions of the CPS.)

- The term "CABI", as used throughout, refers to (typically C/C++/Fortran) code compiled to the machine's native instruction set and using the platform's usual format for such binaries (ELF, PE32, etc.).

.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..

.. _Common Language Runtime: https://en.wikipedia.org/wiki/Common_Language_Runtime

.. _Instruction Set Architecture: https://en.wikipedia.org/wiki/Instruction_set_architecture

.. _Java: https://en.wikipedia.org/wiki/Java_%28programming_language%29

.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..

.. |null| replace:: :keyword:`null`

.. |string| replace:: :type:`string`

.. |list| replace:: :type:`list`

.. |string-list| replace:: |list| of |string|

.. |map| replace:: :type:`map` of |string|

.. |language-string-list| replace:: |string-list| :separator:`or` |map| to |string-list|

.. |package| replace:: :object:`package`

.. |platform| replace:: :object:`platform`

.. |requirement| replace:: :object:`requirement`

.. |component| replace:: :object:`component`

.. |configuration| replace:: :object:`configuration`

.. kate: hl reStructuredText
