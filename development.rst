Development Process
===================

The specification is curated by the editor in chief
(currently Matthew Woehlke)
and is maintained in a `github repository`_.

Community Involvement
'''''''''''''''''''''

Development of the specification
is intended to be an open process.
Contributions are welcome from anyone.
Problems or feature requests
should be filed against the GitHub project.

Much activity and discussion takes place on GitHub,
and we encourage use of Issues and Discussions
as a primary communication channel.
Some members of the community are active
in the #ecosystem_evolution channel
of `CppLang's Slack <https://cpplang.slack.com>`_.
We can also be reached via our `mailing list`_.

In addition, the ecosystem evolution group
typically has at least one monthly video-conference call.
While not strictly limited to CPS discussion,
matters regarding the specification are sometimes discussed there.
Additional, more CPS-focused meetings may also occur.
See the `mailing list`_ for details.

Contributing
''''''''''''

Pull requests are welcome,
but please be aware that changes
which have not been previously discussed
may not be desirable, and may be rejected.
At a minimum, if you submit a pull request
that has not been previously discussed,
it is likely that you will be asked to make changes
before your proposal is accepted.

When editing the documentation,
please keep in mind that whitespace,
and line breaks in particular,
are not meaningful to the generated HTML.
Accordingly, it is preferred to use these
in a way that aims to reduce diff churn
if and when the text is subsequently revised.
Therefore, do not try to use all available space
or slavishly wrap at a particular column.
Rather, keep lines shorter
and try to break at "natural" boundaries,
and **always** break after a sentence.
As a semi-hard limit, reST text
should avoid exceeding 79 characters on a line;
however, "properly" broken lines
should rarely approach that limit.

Commits
^^^^^^^

Commit messages shall consist of a one-line summary,
a blank line, and a longer description.
Summaries should ideally be 50 characters or less,
should start with a capital letter when possible,
should generally omit trailing punctuation,
and should use imperative, present tense.
Descriptions shall be wrapped at 72 characters
except in cases where this is not possible
(e.g. very long hyperlinks).

Commits should be self-contained and complete,
and ideally each distinct change should be a separate commit.
"Fixup" commits should be avoided whenever possible,
and especially should not appear in a branch
when fixing something earlier in the branch.
(The maintainers can and will squash pull requests if needed,
but be aware that "dirty" history in a pull request
makes for additional work all around.)

Following a consistent style for commit messages
helps ensure that commit messages are useful
and makes reading the history more pleasant.
Producing "clean" history also makes it easier
to look back and understand change over time,
as changes are presented in logical units
with as little noise and clutter as possible.

.. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... .. ... ..

.. _github repository: https://github.com/cps-org/cps

.. _mailing list: https://groups.google.com/g/cxx-ecosystem-evolution/about

.. kate: hl reStructuredText
