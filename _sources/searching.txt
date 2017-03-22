Package Searching
=================

Tools shall locate a package by searching for a file :var:`name`\ :path:`.cps` or :var:`name`\ :path:`-`\ :glob:`*`\ :path:`.cps` (where the asterisk (``*``) is one or more characters excluding colon (``:``) and at-sign (``@``), allowing ``.cps`` files to supply a version number as part of their name so that multiple versions may be co-installed) in the following paths:

- :var:`prefix`\ :path:`/cps/` :applies-to:`(Windows)`
- :var:`prefix`\ :path:`/`\ :var:`name`\ :path:`.framework/Resources/CPS/` :applies-to:`(MacOS)`
- :var:`prefix`\ :path:`/`\ :var:`name`\ :path:`.framework/Versions/`\ :glob:`*`\ :path:`/Resources/CPS/` :applies-to:`(MacOS)`
- :var:`prefix`\ :path:`/`\ :var:`name`\ :path:`.app/Contents/Resources/CPS/` :applies-to:`(MacOS)`
- :var:`prefix`\ :path:`/`\ :var:`libdir`\ :path:`/cps/`\ :var:`name`\ :path:`/`\ :glob:`*`\ :path:`/`
- :var:`prefix`\ :path:`/`\ :var:`libdir`\ :path:`/cps/`\ :var:`name`\ :path:`/`
- :var:`prefix`\ :path:`/`\ :var:`libdir`\ :path:`/cps/`
- :var:`prefix`\ :path:`/share/cps/`\ :var:`name`\ :path:`/`\ :glob:`*`\ :path:`/`
- :var:`prefix`\ :path:`/share/cps/`\ :var:`name`\ :path:`/`
- :var:`prefix`\ :path:`/share/cps/`

The placeholder :var:`name` shall represent the name of the package to be located, and shall include both the proper case name, and the name converted to lower case. The placeholder :var:`libdir` shall be the platform defined directories, sans root prefix, in which matching architecture and/or architecture-neutral libraries reside (e.g. :path:`lib`, :path:`lib32`, :path:`lib64`, :path:`lib/i386-linux-gnu`...). The placeholder :var:`prefix` shall represent one of the set of default install prefixes to be searched, which shall include, at minimum and in order, the set of paths (separated by :path:`;` on Windows, :path:`:` otherwise) in the environment variable :env:`CPS_PATH`, :path:`/usr/local`, and :path:`/usr`. In addition, for all such package-neutral prefixes :var:`prefix-root`, the package-specific prefix :var:`prefix-root`\ :path:`/`\ :var:`name` shall also be considered.
The complete list of search paths, above, shall be considered in the order specified above, for each prefix, before the next prefix is searched. Package-specific prefixes shall be searched before package-neutral prefixes.

It is recommended that tools should also provide a mechanism for specifying the path to a specific CPS which may be used to override the default search, or to provide the location of a package which is not installed to any of the standard search paths.

When a candidate ``.cps`` file is found, the tool shall inspect the package's `Platform`_. If the package's platform does not match the target platform, the tool should ignore the ``.cps`` and continue the search. This allows for the installation of packages for different platforms (e.g. 32- and 64-bit builds) on a single machine. (Note that it is up to the tool to determine what constitutes a matching platform.)

Prefix Determination
''''''''''''''''''''

In order to determine the package prefix, which may appear in various attributes as ``@prefix@``, it is necessary to determine the effective prefix from the canonical location of the ``.cps`` file. This can be accomplished in three ways:

- If the package specifies a :attribute:`Cps-Path`, that value shall be used.
- Otherwise, if the tool has just completed a search for the ``.cps``, as described above, the prefix is known from the path which was searched.
- Otherwise, the prefix shall be deduced as follows:

  - The path is initially taken to be the directory portion (i.e. without file name) of the absolute path to the ``.cps`` file.
  - :applies-to:`(MacOS)` If the tail-portion matches :path:`/Resources/` or :path:`/Resources/CPS/`, then:

    - The matching portion is removed.
    - If the tail-portion of the remaining path matches :path:`/Versions/`\ :glob:`*`\ :path:`/`, that portion is removed.
    - If the tail-portion of the remaining path matches :path:`/`\ :var:`name`\ :path:`.framework/` or :path:`/`\ :var:`name`\ :path:`.app/Contents/`, that portion is removed.

  - Otherwise:

    - If the tail-portion of the path matches any of :path:`/cps/`, :path:`/`\ :var:`name`\ :path:`/cps/` or :path:`/cps/`\ :var:`name`\ :path:`/`, the longest such matching portion is removed.
    - If the tail-portion of the remaining path matches any of :path:`/`\ :var:`libdir`\ :path:`/` or :path:`/share/`, that portion is removed.

.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..

.. kate: hl reStructuredText
