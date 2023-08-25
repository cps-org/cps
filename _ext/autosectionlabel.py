"""
    sphinx.ext.autosectionlabel
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Allow reference sections by :ref: role using its title.

    :copyright:
        Copyright 2007-2022 by the Sphinx team,
        see https://github.com/sphinx-doc/sphinx/blob/master/AUTHORS.

        Copyright 2017-2023 Matthew Woehlke, see AUTHORS.

    :license:
        BSD, see LICENSE.BSD for details.
"""

from typing import cast

from docutils import nodes

from sphinx.domains.std import StandardDomain
from sphinx.util import logging
from sphinx.util.nodes import clean_astext

logger = logging.getLogger(__name__)

#==============================================================================
def register_sections_as_label(app, document):
    domain = cast(StandardDomain, app.env.get_domain('std'))
    for node in document.findall(nodes.section):
        labelid = node['ids'][0]
        docname = app.env.docname
        title = cast(nodes.title, node[0])
        name = nodes.fully_normalize_name(title.astext())
        sectname = clean_astext(title)

        if name in domain.labels:
            logger.warning('duplicate label %s, other instance in %s',
                           name, app.env.doc2path(domain.labels[name][0]),
                           location=node)

        domain.anonlabels[name] = docname, labelid
        domain.labels[name] = docname, labelid, sectname

#==============================================================================
def setup(app):
    app.connect('doctree-read', register_sections_as_label)
