Package Configurations
======================

Configurations provide a mechanism for a package to provide multiple configurations from a single distribution. Such configurations might include separate debug and release libraries, builds with and without thread safety, and so forth. The possible configurations are determined by each individual package, and it is left to the consumer and build system to decide when and how to select a non-default configuration.

When a consumer consumes a component, the build system must determine the attribute values for that component by selecting which configuration of the component to use (if the component has multiple configurations). It is recommended that build systems select a configuration as follows:

- For each package, the consumer shall have a mechanism for providing a list of preferred configurations. The first configuration in this list which matches an available configuration of the component shall be used. (If the build system supports multiple configurations, it is recommended that the consuming project may specify different values and/or order of this list depending on its own active configuration.)
- If the build system supports multiple configurations, the build system may implement a mechanism to prefer a configuration which "matches" the consuming project's active configuration.
- The package's `Configurations (Package)`_ shall be searched. The first configuration in this list which matches an available configuration of the component shall be used.

The value of an attribute for a component is determined in one of two ways: If the selected :object:`configuration` of the :object:`component` has the attribute, that value is used. Otherwise, if the :object:`component` directly has the requested attribute, that value is used. This allows a configuration-specific attribute to override an attribute value that is not configuration-specific. If the attribute is required, and is not present on either the selected :object:`configuration`, or the non-configuration-specific attributes of the :object:`component`, then the CPS is ill-formed. Note that a value of :keyword:`null` satisfies the condition of having the attribute. A value of :keyword:`null` has the usual meaning where :keyword:`null` is an acceptable value for the attribute; otherwise, a value of :keyword:`null` shall be treated as the attribute being unset (and shall suppress falling back to the non-configuration-specific value).

Configuration Merging
'''''''''''''''''''''

Some build systems may desire to output separate specifications per configuration, and/or to output separate CPS files per component. This is especially useful to permit piecemeal installation of individual components and/or configurations (for example, a "base" package with release libraries and common components, an optional package with debug libraries, and another optional package with optional components).

When a tool locates a CPS file, :var:`name`\ :path:`.cps`, the tool shall look in the same directory for any files named :var:`name`\ :path:`:`\ :glob:`*`\ :path:`.cps`,  :var:`name`\ :path:`@`\ :glob:`*`\ :path:`.cps`, and :var:`name`\ :path:`:`\ :glob:`*`\ :path:`@`\ :glob:`*`\ :path:`.cps` (the asterisk (``*``) represents file globbing). If any such package specifications are found, they shall be loaded at the same time, and their contents appended to the information loaded from the base CPS.

A ``.cps`` file whose name contains ``@`` is a configuration-specific CPS. The structure of a configuration-specific CPS is the same as a common CPS, with three exceptions:

- The per-configuration specification must contain the `Configuration`_ attribute.
- The per-configuration specification may not specify any :object:`component` attributes (e.g. :attribute:`Type`).
- An attribute on a :object:`component` is considered to belong instead to the component-configuration identified by the configuration-specific CPS.

The order in which the data from multiple CPS files is appended is implementation-defined.

.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..

.. kate: hl reStructuredText