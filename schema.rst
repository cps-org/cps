Package Schema
==============

Objects
'''''''

.. ----------------------------------------------------------------------------
.. cps:object:: package

  The root of a CPS document is a |package| object.
  A |package| object describes a single package.

.. ----------------------------------------------------------------------------
.. cps:object:: platform

  A |platform| describes the platform
  on which a package's components may run.

.. ----------------------------------------------------------------------------
.. cps:object:: requirement

  A |requirement| describes the specifics of a package dependency.

.. ----------------------------------------------------------------------------
.. cps:object:: component

  A |component| is a consumable part of a package.
  Typical components include libraries and executables.

.. ----------------------------------------------------------------------------
.. cps:object:: configuration

  A |configuration| holds attributes
  that are specific to a particular configuration of a |component|.

Attributes
''''''''''

An optional attribute may have the value |null|.
This shall be equivalent to omitting the attribute.

Attribute names are case sensitive.

.. ----------------------------------------------------------------------------
.. cps:attribute:: c_runtime_vendor
  :type: string
  :context: platform

  Specifies that the package's CABI components
  require the specified C standard/runtime library.
  Typical (case-insensitive) values include
  :string:`"bsd"` (libc),
  :string:`"gnu"` (glibc),
  :string:`"mingw"` and
  :string:`"microsoft"`.

.. ----------------------------------------------------------------------------
.. cps:attribute:: c_runtime_version
  :type: string
  :context: platform

  Specifies the minimum C standard/runtime library version
  required by the package's CABI components.

.. ----------------------------------------------------------------------------
.. cps:attribute:: clr_vendor
  :type: string
  :context: platform

  Specifies that the package's CLR (.NET) components
  require the specified `Common Language Runtime`_ vendor.
  Typical (case-insensitive) values include
  :string:`"microsoft"` and
  :string:`"mono"`.

.. ----------------------------------------------------------------------------
.. cps:attribute:: clr_version
  :type: string
  :context: platform

  Specifies the minimum `Common Language Runtime`_ version
  required to use the package's CLR (.NET) components.

.. ----------------------------------------------------------------------------
.. cps:attribute:: compat_version
  :type: string
  :context: package

  Specifies the oldest version of the package
  with which this version is compatible.
  This information is used when a consumer requests a specific version.
  If the version requested is equal to or newer
  than the :attribute:`compat_version`,
  the package may be used.

  If not specified,
  the package is not compatible with previous versions
  (i.e. :attribute:`compat_version`
  is implicitly equal to :attribute:`version`).

.. ----------------------------------------------------------------------------
.. cps:attribute:: compile_features
  :type: list(string)
  :context: component configuration

  Specifies a list of `Compiler Features`_
  that must be enabled or disabled
  when compiling code that consumes the component.

.. ----------------------------------------------------------------------------
.. cps:attribute:: compile_flags
  :type: list(string)|map(list(string))
  :context: component configuration

  Specifies a list of additional flags
  that must be supplied to the compiler
  when compiling code that consumes the component.
  Note that compiler flags may not be portable;
  use of this attribute is discouraged.

  A map may be used instead to give different values
  depending on the language of the consuming source file.
  Handling of such shall be the same as for `definitions`_.

.. ----------------------------------------------------------------------------
.. cps:attribute:: compile_requires
  :type: list(string)
  :context: component configuration

  Specifies additional components required by a component
  which are needed only at the compile stage.
  Unlike `requires (component)`_,
  only the required components' compilation-related attributes
  should be applied transitively;
  link requirements of the required component(s) should be ignored.

  This is especially useful for libraries
  whose interfaces rely on the data types of a dependency
  but do not expose linkable symbols of that dependency,
  or which dynamically load the dependency at run-time.

.. ----------------------------------------------------------------------------
.. cps:attribute:: components
  :type: map(component)
  :context: package
  :overload:
  :required:

  Specifies the components which the package provides.
  Keys are the component names.

.. ----------------------------------------------------------------------------
.. cps:attribute:: components
  :type: list(string)
  :context: requirement
  :overload:

  Specifies a list of components
  which must be present in the required package
  in order for the requirement to be satisfied.
  Although the build tool will generally produce an error
  if a consumer uses a component
  which in turn requires a component that was not found,
  early specification via this attribute
  may help build tools to diagnose such issues earlier
  and/or produce better diagnostics.

  This may also be used to specify dependencies
  that are not expressed in component level dependencies,
  such as a package's requirement
  that a dependency includes a certain symbolic component,
  or if a dependency is only expressed at run-time.

.. ----------------------------------------------------------------------------
.. cps:attribute:: configuration
  :type: string
  :context: package
  :conditionally-required:

  Specifies the name of the configuration
  described by a configuration-specific ``.cps``
  (see `Configuration Merging`_).
  This attribute is required in a configuration-specific ``.cps``,
  and shall be ignored otherwise.

.. ----------------------------------------------------------------------------
.. cps:attribute:: configurations
  :type: list(string)
  :context: package
  :overload:

  Specifies the configurations that are preferred.
  See `Package Configurations`_ for a description
  of how configurations are used.

.. ----------------------------------------------------------------------------
.. cps:attribute:: configurations
  :type: map(configuration)
  :context: component
  :overload:

  Specifies a set of configuration-specific attributes for a |component|.
  Keys are the configuration names.

.. ----------------------------------------------------------------------------
.. cps:attribute:: cpp_runtime_vendor
  :type: string
  :context: platform

  Specifies that the package's CABI components
  require the specified C++ standard/runtime library.
  Typical (case-insensitive) values include
  :string:`"gnu"` (libstdc++),
  :string:`"llvm"` (libc++) and
  :string:`"microsoft"`.

.. ----------------------------------------------------------------------------
.. cps:attribute:: cpp_runtime_version
  :type: string
  :context: platform

  Specifies the minimum C++ standard/runtime library version
  required by the package's CABI components.

.. ----------------------------------------------------------------------------
.. cps:attribute:: cpp_module_metadata
  :type: string
  :context: component configuration

  Specifies the path to a C++ module metadata file
  (also known as a "P3286_" file)
  necessary for consuming C++ interface units for pre-built libraries.

.. ----------------------------------------------------------------------------
.. cps:attribute:: cps_path
  :type: string
  :context: package

  Specifies the directory portion location of the ``.cps`` file.
  This shall be an "absolute" path which starts with ``@prefix@``.
  This provides a mechanism by which the tool
  may deduce the prefix of a relocatable package
  from the absolute location of the ``.cps`` file
  (which will be known by the tool).
  See also `Prefix Determination`_ for details.

  Exactly **one** of ``cps_path`` or `prefix`_ is required.

.. ----------------------------------------------------------------------------
.. cps:attribute:: cps_version
  :type: string
  :context: package
  :required:

  Specifies the version of the CPS
  to which this ``.cps`` file conforms.
  This may be used by tools to provide backwards compatibility
  in case of compatibility-breaking changes in the CPS.

  CPS version numbering follows |semver|_.
  That is, tools that support CPS version ``<X>.<Y>``
  are expected to be able to read files
  with :attribute:`cps_version` ``<X>.<Z>``,
  even for Z > Y
  (with the understanding that, in such cases, the tool
  may miss non-critical information that the CPS provided).

.. ----------------------------------------------------------------------------
.. cps:attribute:: default_components
  :type: list(string)
  :context: package

  Specifies a list of components that should be inferred
  if a consumer specifies a dependency on a package,
  but not a specific component.

.. ----------------------------------------------------------------------------
.. cps:attribute:: definitions
  :type: map(map(string|null))
  :context: component configuration

  Specifies a collection of compile definitions that must be defined
  when compiling code that consumes the component.
  Each key in the inner map(s) is the name of a compile definition,
  such that e.g. ``-Dkey=value`` is passed to the compiler.
  A value may be |null|, indicating a definition with no value
  (e.g. ``-Dkey`` is passed to the compiler).
  Note that an *empty* string indicates ``-Dkey=``,
  which may have a different effect than ``-Dkey``.

  The outer map is used to describe
  language-specific definitions.
  The build tool shall include
  only those definitions
  whose language matches (case-sensitive)
  that of the (lower case) language
  of the source file being compiled.
  Recognized languages shall include
  :string:`"c"`,
  :string:`"cpp"`, and
  :string:`"fortran"`.
  Additionally, the value :string:`"*"` indicates
  that the corresponding definitions apply to all languages.

  If a definition name is repeated
  in both :string:`"*"` and a specific language,
  the latter, when applicable to the source being compiled,
  shall have precedence.

.. ----------------------------------------------------------------------------
.. cps:attribute:: hints
  :type: list(string)
  :context: requirement

  Specifies a list of paths
  where a required dependency might be located.
  When given, this will usually provide the location
  of the dependency as it was consumed by the package
  when the package was built,
  so that consumers can easily find (correct) dependencies
  if they are in a location that is not searched by default.

.. ----------------------------------------------------------------------------
.. cps:attribute:: includes
  :type: list(string)|map(list(string))
  :context: component configuration

  Specifies a list of directories
  which should be added to the include search path
  when compiling code that consumes the component.
  If a path starts with ``@prefix@``,
  the package's prefix is substituted
  (see `Package Searching`_).
  This is recommended, as it allows packages to be relocatable.

  A map may be used instead to give different values
  depending on the language of the consuming source file.
  Handling of such shall be the same as for `definitions`_.

.. ----------------------------------------------------------------------------
.. cps:attribute:: isa
  :type: string
  :context: platform

  Specifies that the package's CABI components
  require the specified `Instruction Set Architecture`_.
  The value is case insensitive
  and should follow the output of ``uname -m``.

.. ----------------------------------------------------------------------------
.. cps:attribute:: jvm_vendor
  :type: string
  :context: platform

  Specifies that the package's Java components
  require the specified Java_ vendor.
  Typical (case-insensitive) values include
  :string:`"oracle"` and
  :string:`"openjdk"`.

.. ----------------------------------------------------------------------------
.. cps:attribute:: jvm_version
  :type: string
  :context: platform

  Specifies the minimum Java_ Virtual Machine version
  required to use the package's Java components.

.. ----------------------------------------------------------------------------
.. cps:attribute:: kernel
  :type: string
  :context: platform

  Specifies the name of the operating system kernel
  required by the package's components.
  The value is case insensitive
  and should follow the output of ``uname -s``.
  Typical values include
  :string:`"windows"`,
  :string:`"cygwin"`,
  :string:`"linux"` and
  :string:`"darwin"`.

.. ----------------------------------------------------------------------------
.. cps:attribute:: kernel_version
  :type: string
  :context: platform

  Specifies the minimum operating system kernel version
  required by the package's components.

.. ----------------------------------------------------------------------------
.. cps:attribute:: link_features
  :type: list(string)
  :context: component configuration

  Specifies a list of `Linker Features`_
  that must be enabled or disabled
  when linking code that consumes the component.

.. ----------------------------------------------------------------------------
.. cps:attribute:: link_flags
  :type: list(string)
  :context: component configuration

  Specifies a list of additional flags
  that must be supplied to the linker
  when linking code that consumes the component.
  Note that linker flags may not be portable;
  use of this attribute is discouraged.

.. ----------------------------------------------------------------------------
.. cps:attribute:: link_languages
  :type: list(string)
  :context: component configuration
  :default: ["c"]

  Specifies the ABI language or languages of a static library
  (`type`_ :string:`"archive"`).
  Officially supported (case-insensitive) values are
  :string:`"c"` (no special handling required) and
  :string:`"cpp"` (consuming the static library
  also requires linking against the C++ standard runtime).

.. ----------------------------------------------------------------------------
.. cps:attribute:: link_libraries
  :type: list(string)
  :context: component configuration

  Specifies a list of additional libraries that must be linked against
  when linking code that consumes the component.
  (Note that packages should avoid using this attribute if at all possible.
  Use `requires (component)`_ instead whenever possible.)

.. ----------------------------------------------------------------------------
.. cps:attribute:: link_location
  :type: string
  :context: component configuration

  Specifies an alternate location of the component
  that should be used when linking against the component.
  This attribute typically applies only to :string:`"dylib"` components
  on platforms where the library is separated into multiple file components.
  For example, on Windows,
  this attribute shall give the location of the ``.lib``,
  while `location`_ shall give the location of the ``.dll``.

  If the path starts with ``@prefix@``,
  the package's prefix is substituted
  (see `Package Searching`_).
  This is recommended, as it allows packages to be relocatable.

.. ----------------------------------------------------------------------------
.. cps:attribute:: link_requires
  :type: list(string)
  :context: component configuration

  Specifies additional components required by a component
  which are needed only at the link stage.
  Unlike `requires (component)`_,
  only the required components' link dependencies
  should be applied transitively;
  additional properties such as compile and include attributes
  of the required component(s) should be ignored.

.. ----------------------------------------------------------------------------
.. cps:attribute:: location
  :type: string
  :context: component configuration
  :conditionally-required:

  Specifies the location of the component.
  The exact meaning of this attribute
  depends on the component type,
  but typically it provides the path
  to the component's primary artifact,
  such as a ``.so`` or ``.jar``.
  (For Windows DLL components,
  this should be the location of the ``.dll``.
  See also `link_location`_.)

  If the path starts with ``@prefix@``,
  the package's prefix is substituted
  (see `Package Searching`_).
  This is recommended, as it allows packages to be relocatable.

  This attribute is required for |component|\ s
  that are not of :string:`"interface"` :attribute:`type`.

.. ----------------------------------------------------------------------------
.. cps:attribute:: name
  :type: string
  :context: package
  :required:

  Specifies the canonical name of the package.
  In order for searching to succeed,
  the name of the CPS file
  without the ``.cps`` suffix
  must exactly match (including case)
  either :attribute:`name` as-is,
  or :attribute:`name` converted to lower case.

.. ----------------------------------------------------------------------------
.. cps:attribute:: platform
  :type: platform
  :context: package

  Specifies the platform on which a package's components may run.
  This allows tools to ignore packages
  which target a different platform
  than the platform that the consumer targets
  (see `Package Searching`_).
  Any platform attribute not specified
  implies that the package's components
  are agnostic to that platform attribute.
  If this attribute is not specified,
  the package is implied to be platform agnostic.
  (This might be the case for a "library"
  which consists entirely of C/C++ headers.
  Note that JVM/CLR versions are platform attributes,
  so packages consisting entirely of Java and/or CLR components
  will still typically use this attribute.)

.. ----------------------------------------------------------------------------
.. cps:attribute:: prefix
  :type: string
  :context: package

  Specifies the package's prefix
  for non-relocatable package.
  See also `Prefix Determination`_.

  Exactly **one** of `cps_path`_ or ``prefix`` is required.

.. ----------------------------------------------------------------------------
.. cps:attribute:: requires
  :type: list(string)
  :context: component configuration
  :overload:

  Specifies additional components required by a component.
  This is used, for example, to indicate transitive dependencies.
  Relative component names are interpreted relative to the current package.
  Absolute component names must refer to a package required by this package
  (see `requires (package)`_).
  Compile and link attributes should be applied transitively,
  as if the consuming component also directly consumed the components
  required by the component being consumed.

  See also `link_requires`_.

.. ----------------------------------------------------------------------------
.. cps:attribute:: requires
  :type: map(requirement)
  :context: package
  :overload:

  Specifies additional packages that are required by this package.
  Keys are the name of another required package.
  Values are a valid |requirement| object or |null|
  (equivalent to an empty |requirement| object)
  describing the package required.

.. ----------------------------------------------------------------------------
.. cps:attribute:: type
  :type: string
  :context: component
  :required:

  Specifies the type of a component.
  The component type affects how the component may be used.
  Officially supported values are :string:`"executable"`
  (any artifact which the target platform can directly execute),
  :string:`"archive"` (CABI static library),
  :string:`"dylib"` (CABI shared library),
  :string:`"module"` (CABI plugin library),
  :string:`"jar"` (Java Archive),
  :string:`"interface"` and :string:`"symbolic"`.
  If the type is not recognized by the parser,
  the component shall be ignored.
  (Parsers are permitted to support additional types
  as a conforming extension.)

  A :string:`"dylib"` is meant to be linked at compile time;
  the :attribute:`location` specifies the artifact
  required for such linking (i.e. the import library on PE platforms).
  A :string:`"module"` is meant to be loaded at run time
  with :code:`dlopen` or similar;
  again, the :attribute:`location` specifies the appropriate artifact.

  An :string:`"interface"` component is a special case;
  it may have the usual attributes of a component,
  but does not have a location.
  This can be used to create "virtual" components
  that do not have an associated artifact.

  A :string:`"symbolic"` component is even more special,
  as it has no (required) attributes at all,
  and the meaning of any attributes or configurations
  assigned to such a component is unspecified.
  A :string:`"symbolic"` component is intended
  to be used as a form of feature testing;
  a package that has a feature that is meaningful to users
  but does not otherwise map directly to a component
  may use a symbolic component
  to indicate availability of the feature to users.

.. ----------------------------------------------------------------------------
.. cps:attribute:: version
  :type: string
  :context: package
  :overload:

  Specifies the version of the package.
  The format of this string is determined by `version_schema`_.

  If not provided, the CPS will not satisfy any request
  for a specific version of the package.

.. ----------------------------------------------------------------------------
.. cps:attribute:: version
  :type: string
  :context: requirement
  :overload:

  Specifies the required version of a package.
  If omitted, any version of the required package is acceptable.
  Semantics are the same
  as for the :attribute:`version` attribute of a |package|.

.. ----------------------------------------------------------------------------
.. cps:attribute:: version_schema
  :type: string
  :context: package
  :default: "simple"

  Specifies the structure
  to which the package's version numbering conforms.
  Tools may use this to determine how to perform version comparisons.
  Officially supported (case-insensitive) values are
  :string:`"simple"` and :string:`"custom"`
  (:string:`"rpm"` or :string:`"dpkg"` should be used where applicable,
  but may not be supported by all tools).
  If a package uses :string:`"custom"`,
  version numbers may be compared,
  but version ordering is not possible.

  Needless to say,
  changing a package's version scheme between releases
  is *very strongly discouraged*.

  Note that this attribute determines
  only how version numbers are *ordered*.
  It does not imply anything
  about the compatibility or incompatibility
  of various versions of a package.
  See also `compat_version`_.

  - :string:`simple`

    The package's version number
    shall match the regular expression
    ``[0-9]+([.][0-9]+)*([-+].*)?``.

    The portion of the version
    which precedes the optional ``-`` or ``+``
    may be interpreted as a tuple of integers,
    in which leading zeros are ignored.
    Version numbers are compared according to numerical order,
    starting from the first (left-most) number of the tuples.
    If two version numbers have different tuple sizes,
    the shorter tuple shall be implicitly filled with zeros.

  .. deprecated:: 0.9.0

      :string:`"semver"` is a deprecated alias for :string:`"simple"`.

Notes
'''''

- Unless otherwise specified,
  a relative file path appearing in a CPS
  shall be interpreted relative to the ``.cps`` file.

- Unless otherwise specified,
  unrecognized attributes shall be ignored.
  This makes it easier for tools to add tool-specific extensions.
  (It is *strongly* recommended that the names of any such attributes
  start with ``x_<tool>_``, where ``<tool>`` is the (lower case) name
  of the tool which introduced the extension,
  in order to reduce the chance of conflicts
  with newer versions of the CPS.)

- The term "CABI", as used throughout,
  refers to (typically C/C++/Fortran) code
  compiled to the machine's native instruction set
  and using the platform's usual format for such binaries
  (ELF, PE32, etc.).

JSON Schema
'''''''''''

A `JSON Schema`_ for CPS can be obtained :schema:`here`.
The schema is generated from this documentation,
and is intended to be used for machine validation of CPS files.
In case of discrepancies, this documentation takes precedence.
(That said, issue reports are welcomed and strongly encouraged;
please refer to our `Development Process`_.)

.. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... ..

.. _Common Language Runtime: https://en.wikipedia.org/wiki/Common_Language_Runtime

.. _Instruction Set Architecture: https://en.wikipedia.org/wiki/Instruction_set_architecture

.. _Java: https://en.wikipedia.org/wiki/Java_%28programming_language%29

.. _JSON Schema: https://json-schema.org/

.. _semver: http://semver.org/

.. _P3286: https://wg21.link/p3286

.. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... ..

.. |semver| replace:: Semantic Versioning

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

.. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... ..

.. kate: hl reStructuredText
