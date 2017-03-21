Component Specification
=======================

Package, component and configuration names may consist of ASCII letters, numbers, hyphens (``-``), and underscores (``_``), and may not contain forward-stroke (``/``) or at-sign (``@``). Colon (``:``) may be used in component and configuration names, but not package names. The behavior of other characters is implementation defined. Portable packages are recommended to use only those characters which are expressly permitted.

A CPS component specification consists of either a package name, component name, or package-component name, either of which may optionally specify a configuration. A colon (``:``) is used to separate a package name from a component name, and always precedes a component name without a package name. A component specification including a package name is an "absolute" name. A component specification without a package name is a "relative" name; the package name in such case is implicitly the same as the package specification in which such name appears. The package and/or component name may be followed by the at-sign (``@``) and a configuration name. The special case of using the at-sign as a configuration name (e.g. ``foo:foo-core@@``) means that the named configuration is the same as the configuration in which the name appears. (For example, the component ``foo-ui`` has non-configuration-specific :attribute:`Requires` :string:`":foo-core@@"` and :attribute:`Configurations` :string:`"A"` and :string:`"B"`. The :string:`"A"` configuration of ``foo-ui`` therefore requires ``:foo-core@A``, and similar for other configurations.)

If a requirement does not specify a configuration, the *consumer* chooses the most appropriate configuration. This allows the consumer to, for example, link to the debug libraries of an indirect dependency when the consumer is build in debug mode, even if the consumer always uses the optimized configuration of the direct dependency.

.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..

.. kate: hl reStructuredText
