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
to the recommendation that extensions use the ``X-`` prefix.

Attributes\ :hidden:`(Supplemental)`
''''''''''''''''''''''''''''''''''''

By definition, none of the following attributes are required.

:attribute:`Default-License`
----------------------------

Specifies the `License`_ that is assumed to apply to a component,
if none is otherwise specified.
This is convenient for packages
that wish their `License`_ to reflect portions of the package
that are not reflected by a component (such as data files)
when most or all of the compiled artifacts use the same license.

:attribute:`Description`
------------------------

:Type: :type:`string`
:Applies To: :object:`package`, :object:`component`

Provides a human readable description of the function
which the package or component provides.

:attribute:`Display-Name`
-------------------------

:Type: :type:`string`
:Applies To: :object:`package`

Provides a human readable name of the package.
If provided, tools may use this in informational messages
instead of, or in addition to, the canonical package name.

:attribute:`License`
--------------------

:Type: Special
:Applies To: :object:`package`, :object:`component`

Specifies the license or licenses
under which the package is distributed.
A :type:`string` value shall be used for a single license.
If multiple licenses need to be specified,
a :type:`list` shall be used.
Each :type:`string` value of the :type:`list`
is a license which *always* applies to the package.
If a package is wholly or partly multi-licensed
(that is, the user has a choice of license),
the top level :type:`list` shall contain a :type:`list` of values
representing possible licenses.
For example, the value ``["CC-BY-4.0", ["GPL-2.0", "LGPL-3.0+"]]``
indicates that some portions of the package
are licensed under :string:`"CC-BY-4.0"`,
while others are licensed as (at the user's choice)
either :string:`"GPL-2.0"` or :string:`"LGPL-3.0+"`.
If necessary, further nesting may be employed;
each nesting level alternates
between inclusive ("A **and** B")
and exclusive ("A **or** B") licensing.

If parts of a package use different licenses,
this attribute may also be specified on a component
if doing so helps to clarifying the licensing.
(See also `Default-License`_.)

License identifiers should follow the |SPDX|_ `License List`_.
The ``WITH`` operator may be used when appropriate,
but structured data is used to express conjunctions and disjunctions,
as described in the preceding paragraph.

:attribute:`Meta-Comment`
-------------------------

:Type: :type:`string`
:Applies To: :object:`package`

Provides a description of the file contents,
for readers that may not be familiar with CPS files.
The typical value is
:string:`"Common Package Specification for <package name>"`.

:attribute:`Meta-Schema`
------------------------

:Type: :type:`string`
:Applies To: :object:`package`

Provides a URI link to a document describing the format of the CPS file.
The typical value is :string:`"https://mwoehlke.github.io/cps/"`
(i.e. the top level page of this site).

:attribute:`Website`
--------------------

:Type: :type:`string`
:Applies To: :object:`package`

Specifies the URI at which the package's website may be found.

.. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... ..

.. _SPDX: https://spdx.org/

.. _License List: https://spdx.org/licenses/

.. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... ..

.. |SPDX| replace:: Software Package Data Exchange

.. kate: hl reStructuredText
