Package Searching
=================

Tools shall locate a package
by searching for a file
:var:`name`\ :path:`.cps`
in the following paths:

- :var:`environment-path`\ :path:`/`\
  :var:`name-like`\ :path:`/cps/`

- :var:`environment-path`\ :path:`/`\
  :var:`name-like`\ :path:`/`

.. raw:: never

    .. This block is used to separate the above and below list items

- :var:`prefix`\ :path:`/`\ :var:`name-like`\ :path:`/cps/`
  :applies-to:`(Windows)`

- :var:`prefix`\ :path:`/cps/`\ :var:`name-like`\ :path:`/`
  :applies-to:`(Windows)`

- :var:`prefix`\ :path:`/cps/`
  :applies-to:`(Windows)`

- :var:`prefix`\ :path:`/`\ :var:`name`\ :path:`.framework/Versions/`\
  :glob:`*`\ :path:`/Resources/CPS/`
  :applies-to:`(macOS)`

- :var:`prefix`\ :path:`/`\ :var:`name`\ :path:`.framework/Resources/CPS/`
  :applies-to:`(macOS)`

- :var:`prefix`\ :path:`/`\ :var:`name`\
  :path:`.app/Contents/Resources/CPS/`
  :applies-to:`(macOS)`

- :var:`prefix`\ :path:`/`\ :var:`libdir`\
  :path:`/cps/`\ :var:`name-like`\ :path:`/`

- :var:`prefix`\ :path:`/`\
  :var:`libdir`\ :path:`/cps/`

- :var:`prefix`\ :path:`/share/cps/`\
  :var:`name-like`\ :path:`/`

- :var:`prefix`\ :path:`/share/cps/`

The various placeholders are as follows:

:var:`name`:
  The name of the package to be located,
  including both the case as specified by the consumer,
  and the name converted to lower case.

:var:`name-like`:
  Any of
  :var:`name`\ :path:`/`\ :glob:`*` or
  :var:`name`,
  where :var:`name` is as previously defined,
  and the asterisk (``*``) is one or more
  valid filename characters, excluding the path separator.
  This is intended to allow multiple versions of a package
  to be installed into the same :var:`prefix`.

:var:`libdir`:
  The platform defined directories, sans root prefix,
  in which matching architecture
  and/or architecture-neutral libraries reside
  (e.g. :path:`lib`, :path:`lib32`, :path:`lib64`,
  :path:`lib/x86_64-linux-gnu`...).

:var:`environment-path`:
  One of the set of paths
  (separated by :path:`;` on Windows, :path:`:` otherwise)
  in the environment variable :env:`CPS_PATH`.
  If :env:`CPS_PATH` is empty,
  paths starting with :var:`environment-path` are skipped.

:var:`prefix`:
  One of the set of default install prefixes to be searched,
  which shall include, at minimum and in order,
  the set of paths (separated by :path:`;` on Windows, :path:`:` otherwise)
  in the environment variable :env:`CPS_PREFIX_PATH`,
  :path:`/usr/local`, and :path:`/usr`.

All paths beginning with :var:`environment-path`
shall be searched in the order specified above,
for each path in :env:`CPS_PATH`,
before the next such path is searched,
and before any other paths are searched.
All paths beginning with :var:`prefix`
shall be searched in the order specified above,
for each prefix, before the next prefix is searched.

It is recommended that tools should also provide
a mechanism for specifying the path to a specific CPS
which may be used to override the default search,
or to provide the location of a package
which is not installed to any of the standard search paths.

When a candidate ``.cps`` file is found,
the tool shall inspect the package's `platform`_.
If the package's platform does not match the target platform,
the tool should ignore the ``.cps`` and continue the search.
This allows for the installation of packages for different platforms
(e.g. 32- and 64-bit builds) on a single machine.
(Note that it is up to the tool to determine
what constitutes a matching platform.)
Similarly, if the package's version
does not satisfy the required version
as specified by the user,
the tool should continue searching.
(In both cases, the tool may wish
to make note of the incompatible packages,
and the reason for rejection.)

Prefix Determination
''''''''''''''''''''

Various attributes may specify relative paths
by use of the ``@prefix@`` placeholder.
In order to resolve these paths,
it is necessary to know the package's prefix
(which may or may not be the same
as :var:`prefix`, above).
This is accomplished in one of two ways:

- If a package specifies `prefix`_, that value is used.

- If a package specifies `cps_path`_,
  the prefix shall be determined from that value
  in combination with the absolute location of the ``.cps`` file.

A correctly specified `cps_path`_ will match the location
(that is, the path without the final ``.cps`` file name)
of the ``.cps`` file.
For example, ``/usr/local/lib/cps/foo/foo.cps``
specifies ``"cps_path": "@prefix@/lib/cps/foo"``.
The absolute location is ``/usr/local/lib/cps/foo``
and the prefix-relative location is ``lib/cps/foo``,
which matches the trailing portion of the absolute location.
Therefore, the prefix is the unmatched portion
of the absolute location, or ``/usr/local``.

If ``fullpath`` is the location of the ``.cps`` file,
tools shall attempt prefix resolution
against ``dirname(fullpath)``, at minimum.
It is recommended that, if this fails,
tools also attempt prefix resolution
against ``realpath(dirname(fullpath))``
and ``dirname(realpath(fullpath))``,
where ``realpath(...)`` represents the canonicalized
(that is, with all symlinks fully expanded)
form of its argument.

.. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... ..

.. kate: hl reStructuredText
