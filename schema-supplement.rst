Supplemental Schema
===================

The `Package Schema`_ describes the normative specification,
which conforming tools are required to support in a prescribed manner.
This section describes additional, optional elements
which are useful, but non-normative.
Conforming tools are not required to be aware of these elements,
but by including them in this supplement,
it is hoped that tools for which these ideas are useful
would operate in a way that allows these elements
to be useful to all tools
that implement functionality along the lines here described.

These can be seen as "officially blessed" exceptions
to the recommendation that extensions use the ``x_`` prefix.

Attributes\ :hidden:`(Supplemental)`
''''''''''''''''''''''''''''''''''''

By definition, none of the following attributes are required.

.. ----------------------------------------------------------------------------
.. cps:attribute:: default_license
  :type: string
  :context: package

  Specifies the `license`_ that is assumed to apply to a component,
  if none is otherwise specified.
  This is convenient for packages
  that wish their `license`_ to reflect portions of the package
  that are not reflected by a component (such as data files)
  when most or all of the compiled artifacts use the same license.

  The value shall be a well formed
  |SPDX|_ `License Expression`_ .

.. ----------------------------------------------------------------------------
.. cps:attribute:: description
  :type: string
  :context: package component

  Provides a human readable description of the function
  which the package or component provides.

.. ----------------------------------------------------------------------------
.. cps:attribute:: display_name
  :type: string
  :context: package

  Provides a human readable name of the package.
  If provided, tools may use this in informational messages
  instead of, or in addition to, the canonical package name.

.. ----------------------------------------------------------------------------
.. cps:attribute:: license
  :type: string
  :context: package component

  Specifies the license or licenses
  under which the package is distributed.
  The value shall be a well formed
  |SPDX|_ `License Expression`_ .

  If parts of a package use different licenses,
  this attribute may also be specified on a component
  if doing so helps to clarifying the licensing.
  (See also `default_license`_.)

.. ----------------------------------------------------------------------------
.. cps:attribute:: meta_comment
  :type: string
  :context: package

  Provides a description of the file contents,
  for readers that may not be familiar with CPS files.
  The typical value is
  :string:`"Common Package Specification for <package name>"`.

.. ----------------------------------------------------------------------------
.. cps:attribute:: meta_schema
  :type: string
  :context: package

  Provides a URI link to a document describing the format of the CPS file.
  The typical value is :string:`"https://cps-org.github.io/cps/"`
  (i.e. the top level page of this site).

.. ----------------------------------------------------------------------------
.. cps:attribute:: website
  :type: string
  :context: package
  :format: uri

  Specifies the URI at which the package's website may be found.

.. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... ..

.. _SPDX: https://spdx.org/

.. _License Expression: https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/

.. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... ..

.. |SPDX| replace:: Software Package Data Exchange

.. kate: hl reStructuredText
