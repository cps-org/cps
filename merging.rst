Description Merging
===================

Some build systems may desire to output
separate specifications per configuration,
and/or to break a package's components into multiple output files,
often according to functional groups.
This is especially useful to permit piecemeal installation
of components and/or configurations
(for example, a "base" package
with release libraries and common components,
an optional package with debug libraries,
and another optional package with optional components).
This also allows build tools to import only those components
which are actually required by a consumer.

When a tool locates a CPS file, :var:`name`\ :path:`.cps`,
the tool shall look in the same directory for any files
which match any of the patterns
(the asterisk (``*``) represents file globbing):

  - :var:`name`\ :path:`:`\ :glob:`*`\ :path:`.cps`

  - :var:`name`\ :path:`-`\ :glob:`*`\ :path:`.cps`

  - :var:`name`\ :path:`@`\ :glob:`*`\ :path:`.cps`

  - :var:`name`\ :path:`:`\ :glob:`*`\ :path:`@`\ :glob:`*`\ :path:`.cps`

  - :var:`name`\ :path:`-`\ :glob:`*`\ :path:`@`\ :glob:`*`\ :path:`.cps`

.. note::

    Patterns containing colon (``:``) shall be skipped
    on platforms for which that character
    is not permitted in file names (e.g. Windows).

If any such package specifications are found,
they shall be loaded at the same time,
and their contents appended to the information loaded from the base CPS.
However, tools are permitted and encouraged
to ignore the information in any such supplemental CPS files
as they may determine is not relevant to the user's needs.
In particular, see `Transitive Dependencies`_.)

A ``.cps`` file whose name contains ``@``
is a configuration-specific CPS.
The structure of a configuration-specific CPS
is the same as a base CPS, with three exceptions:

- The only defined :object:`package` keys are
  `name`_, `cps_version`_, `configuration`_,
  and `components <components\ (package)>`_.
  The first three are required.
  Use of other attributes specified in the schema is ill-formed.

- The per-configuration specification may not specify
  any :object:`component` attributes (e.g. :attribute:`type`).
  Only :object:`configuration` attributes are allowed.

- An attribute on a :object:`component`
  is considered to belong instead
  to the component-configuration
  identified by the configuration-specific CPS.

A ``.cps`` file which supplements the components
of the package's base CPS
is known as an "appendix".
The structure of a CPS appendix
is the same as a base CPS, with two exceptions:

- The only defined :object:`package` keys are
  `name`_, `requires <requires\ (package)>`_, `default_license`_
  and `components <components\ (package)>`_.
  The first is required.
  Use of other attributes specified in the schema is ill-formed.

- An appendix may not specify components
  which are described in the base CPS
  or in any other appendix.

The order in which the data from multiple CPS files is collated
is implementation-defined.
Behavior when a supplemental CPS file's `cps_version`_
differs from the base CPS's version
is implementation-defined.
(However, for obvious reasons,
this is strongly discouraged.)
