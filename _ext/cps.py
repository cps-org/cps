from sphinx import domains
from sphinx import addnodes

from docutils import nodes
from docutils.parsers.rst import directives, roles
from docutils.transforms import Transform

import re

#==============================================================================
class InternalizeLinks(Transform):
    default_priority = 200

    #--------------------------------------------------------------------------
    def apply(self, **kwargs):
        for ref in self.document.traverse(nodes.reference):
            # Skip inter-document links
            if 'refname' in ref:
                if self.document.nameids.get(ref['refname']):
                    continue

            # Convert remaining non-external links to intra-document references
            refuri = ref['refuri'] if 'refuri' in ref else None
            if not refuri or not '://' in refuri:
                # Get the raw text (strip ``s and _)
                rawtext = re.sub('^`(.*)`_?$', '\\1', ref.rawsource)

                # Create xref node
                xref = addnodes.pending_xref(
                    rawtext, reftype='ref', refdomain='std',
                    refexplicit=(refuri is not None))

                # Rewrite section links
                if not refuri:
                    refuri = ref['name']

                # Fill target information
                xref['reftarget'] = refuri.lower()
                xref['refwarn'] = True
                xref['refdoc'] = self.document.settings.env.docname

                # Add ref text
                xref += nodes.inline(rawtext, ref['name'],
                                     classes=ref['classes'])

                # Replace the old node
                ref.replace_self(xref)

#==============================================================================
def add_role(app, name, styles=None, parent=roles.generic_custom_role):
    options = {}
    if styles is None:
        styles=name
    else:
        styles=' '.join([name] + styles)

    options['class'] = directives.class_option(styles)
    role = roles.CustomRole(name, parent, options)
    app.add_role(name, role)

#==============================================================================
def add_code_role(app, name, styles=None, parent=roles.code_role):
    add_role(app, name, styles, parent)

#==============================================================================
def setup(app):
    # Add custom transform to resolve cross-file references
    app.add_transform(InternalizeLinks)

    # Remove built-in 'keyword' role so we can override it
    del app.domains['std'].roles['keyword']

    # Add site-specific custom roles (these just apply styling)
    add_role(app, 'hidden')
    add_role(app, 'applies-to')
    add_role(app, 'separator')
    add_code_role(app, 'object')
    add_code_role(app, 'attribute')
    add_code_role(app, 'feature')
    add_code_role(app, 'feature.opt', styles=['feature', 'optional'])
    add_code_role(app, 'feature.var', styles=['feature', 'var'])
    add_code_role(app, 'keyword')
    add_code_role(app, 'type')
    add_code_role(app, 'string')
    add_code_role(app, 'path')
    add_code_role(app, 'glob')
    add_code_role(app, 'var')
    add_code_role(app, 'env')
