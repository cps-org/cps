Package Configurations
======================

Configurations allow packages to provide
multiple "flavors" of binary objects
in a single distribution,
which have been compiled using different options
to facilitate different use cases.
Nominally, such objects must be *type-homogeneous*,
meaning all configurations of a component
must be of the same `type`_.
(See `Multi-Axis Configurations`_
for a way to work around this restriction;
however, be aware of the caveats described therein.)

Typical configuration axes include
presence or omission of instrumentation code,
optimization level,
and selection of interchangeable implementations.
The possible configurations
are determined by each individual package,
and it is left to the consumer and build system
to decide when and how to select a non-default configuration.
Refer to `Configuration Use Cases`_ for guidance
on what should or should not be expressed as a configuration.

Like appendices, configurations support partial installation.
This allows a package to be built in several configurations,
while permitting users to install only one desired configuration.
Refer to `Description Merging`_ for additional information.

Configuration Selection
'''''''''''''''''''''''

When a consumer consumes a component,
the build system must determine the attribute values for that component
by selecting which configuration of the component to use
(if the component has multiple configurations).
Selection shall treat configuration names as case insensitive.
It is recommended that build systems select a configuration as follows:

- For each package, the consumer shall have a mechanism
  for providing a list of preferred configurations.
  The first configuration in this list
  which matches an available configuration of the component
  shall be used.
  (If the build system supports multiple configurations,
  it is recommended that the consuming project
  may specify different values and/or order of this list
  depending on its own active configuration.)

- If the build system supports multiple configurations,
  the build system may implement a mechanism to prefer a configuration
  which "matches" the consuming project's active configuration.

- The package's `configurations (package)`_ shall be searched.
  The first configuration in this list
  which matches an available configuration of the component
  shall be used.

The value of an attribute for a component
is determined in one of two ways:
If the selected :object:`configuration`
of the :object:`component` has the attribute,
that value is used.
Otherwise, if the :object:`component`
directly has the requested attribute,
that value is used.
This allows a configuration-specific attribute
to override an attribute value that is not configuration-specific.
If the attribute is required,
and is not present on either the selected :object:`configuration`,
or the non-configuration-specific attributes of the :object:`component`,
then the CPS is ill-formed.
Note that a value of :keyword:`null`
satisfies the condition of having the attribute.
A value of :keyword:`null` has the usual meaning
where :keyword:`null` is an acceptable value for the attribute;
otherwise, a value of :keyword:`null`
shall be treated as the attribute being unset
(and shall suppress falling back to the non-configuration-specific value).

.. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... ..

.. kate: hl reStructuredText
