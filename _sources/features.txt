Compiler and Linker Features
============================

CPS supports a notion of compiler and linker "features", which are used to abstract requirements that consumers of a component modify the default compiler and/or linker behavior in order to deal with functional inconsistencies across tools. While it is ultimately up to the build tool to determine how to map features to tool invocation flags, it is clearly beneficial to attempt to standardize a set of "well known" features. Known features shall be case-insensitive, however compiler specific portions might be case sensitive. (For example, :feature:`warn:error` and :feature:`Warn:Error` are the same feature, but :feature:`warn:foo` and :feature:`warn:Foo` should be treated as different, unless the tool has sufficient knowledge of the compiler to know otherwise.)

Compiler Features
'''''''''''''''''

:feature:`c99`
--------------

|code-uses| |c99|. |should-use| |c99| (e.g. ``--std=c99`` or later).

:feature:`c11`
--------------

|code-uses| |c11|. |should-use| |c11| (e.g. ``--std=c11`` or later).

:feature:`c++03`
----------------

|code-uses| |cpp03|. |should-use| |cpp03| (e.g. ``--std=c++03`` or later).

:feature:`c++11`
----------------

|code-uses| |cpp11|. |should-use| |cpp11| (e.g. ``--std=c++11`` or later).

:feature:`c++14`
----------------

|code-uses| |cpp14|. |should-use| |cpp14| (e.g. ``--std=c++14`` or later).

:feature:`c++17`
----------------

|code-uses| |cpp17|. |should-use| |cpp17| (e.g. ``--std=c++17`` or later).

:feature:`gnu`
--------------

The component's public interface makes use of features which are GNU extensions. |should-use| GNU extensions (e.g. ``--std=gnu`` or ``--std=gnu++``).

:feature.opt:`no`\ :feature:`warn:`\ :feature.var:`...`
-------------------------------------------------------

Code using the component should either enable (:feature:`warn`) or disable (:feature:`nowarn`) the specified warning. The warnings are compiler specific, e.g. ``warn:reorder`` (GCC, Clang) or ``warn:4513`` (MSVC).

Tools are expected to recognize if a warning is applicable to the compiler and source language being used (e.g. by attempting to build a test program with the warning in question), and to ignore the feature otherwise.

:feature.opt:`no`\ :feature:`warn:error`
----------------------------------------

Code using the component should either treat all warnings as errors (:feature:`warn:error`), or should not treat warnings as errors (:feature:`nowarn:error`).

:feature.opt:`no`\ :feature:`error:`\ :feature.var:`...`
--------------------------------------------------------

Code using the component should either enable (:feature:`error`) the specified warning, additionally promoting it to an error, or should not treat the specified warning as an error  (:feature:`noerror`). As with :feature.opt:`no`\ :feature:`warn:`\ :feature.var:`...`, the warnings are compiler specific. Note that :feature:`noerror` traditionally does not indicate whether the specified warning should be issued or not, only that if it is issued, it should not be promoted to an error.

Linker Features
'''''''''''''''

:feature:`threads`
------------------

Code using the component should be built with run-time threading support. On Windows, this would typically be used to select the multi-threaded CRT library rather than the single-threaded CRT. On POSIX platforms, it typically indicates that the application should be built with ``-pthread``.

.. TODO do we need `pic`? `sanitize:<...>`?

.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..

.. |code-uses| replace:: The component's public interface makes use of features
                         included in

.. |should-use| replace:: Code using the component should be compiled in a mode
                          which supports

.. |c99| replace:: ISO/IEC 9899:1999
.. |c11| replace:: ISO/IEC 9899:2011
.. |cpp03| replace:: ISO/IEC 14882:2003
.. |cpp11| replace:: ISO/IEC 14882:2011
.. |cpp14| replace:: ISO/IEC 14882:2014
.. |cpp17| replace:: ISO/IEC 14882:2017

.. kate: hl reStructuredText
