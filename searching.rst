Package Searching
=================

Tools shall locate a package
by searching for a file
:var:`name`\ :path:`.cps`
in the following paths:

- :var:`prefix`\ :path:`/cps/`
  :applies-to:`(Windows)`

- :var:`prefix`\ :path:`/cps/`\ :var:`name-like`\ :path:`/`
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
  including both the proper case name,
  and the name converted to lower case.

:var:`name-like`:
  Any of
  :var:`name`\ :path:`/`\ :glob:`*`,
  :var:`name`\ :path:`-`\ :glob:`*`, or
  :var:`name`,
  where :var:`name`: is as previously defined,
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

:var:`prefix`:
  One of the set of default install prefixes to be searched,
  which shall include, at minimum and in order,
  the set of paths (separated by :path:`;` on Windows, :path:`:` otherwise)
  in the environment variable :env:`CPS_PATH`,
  :path:`/usr/local`, and :path:`/usr`.

  In addition,
  for all such package-neutral prefixes :var:`prefix-root`,
  the package-specific prefixes
  :var:`prefix-root`\ :path:`/`\ :var:`name-like`
  shall also be considered.

The complete list of search paths, above,
shall be considered in the order specified above,
for each prefix, before the next prefix is searched.
Package-specific prefixes shall be searched
before package-neutral prefixes.

It is recommended that tools should also provide
a mechanism for specifying the path to a specific CPS
which may be used to override the default search,
or to provide the location of a package
which is not installed to any of the standard search paths.

When a candidate ``.cps`` file is found,
the tool shall inspect the package's `Platform`_.
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

In order to determine the package prefix,
which may appear in various attributes as ``@prefix@``,
it is necessary to determine the effective prefix
from the canonical location of the ``.cps`` file.
This can be accomplished in three ways:

- If the package specifies a :attribute:`Cps-Path`,
  that value shall be used.

- Otherwise, if the tool has just completed a search
  for the ``.cps``, as described above,
  the prefix is known from the path which was searched.

- Otherwise, the prefix shall be deduced as follows:

  - The path is initially taken to be the directory portion
    (i.e. without file name) of the absolute path to the ``.cps`` file.

  - :applies-to:`(macOS)`
    If the tail-portion matches
    :path:`/Resources/` or :path:`/Resources/CPS/`,
    then:

    - The matching portion is removed.

    - If the tail-portion of the remaining path
      matches :path:`/Versions/`\ :glob:`*`\ :path:`/`,
      that portion is removed.

    - If the tail-portion of the remaining path matches
      :path:`/`\ :var:`name`\ :path:`.framework/` or
      :path:`/`\ :var:`name`\ :path:`.app/Contents/`,
      that portion is removed.

  - Otherwise:

    - If the tail-portion of the path matches
      :path:`/cps/`\ :var:`name-like`\ :path:`/` or
      :path:`/cps/`,
      that portion is removed.

    - If the tail-portion of the remaining path matches any of
      :path:`/`\ :var:`libdir`\ :path:`/` or :path:`/share/`,
      that portion is removed.

.. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... ..

.. kate: hl reStructuredText
