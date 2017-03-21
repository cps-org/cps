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
def add_role(app, name, styles=[], parent=roles.generic_custom_role):
    options = {}
    if len(styles):
        options['class'] = directives.class_option(styles) # FIXME??
    else:
        options['class'] = directives.class_option(name)

    role = roles.CustomRole(name, parent, options)
    app.add_role(name, role)

#==============================================================================
def setup(app):
    # Add custom transform to resolve cross-file references
    app.add_transform(InternalizeLinks)

    # Remove built-in 'keyword' role so we can override it
    del app.domains['std'].roles['keyword']

    # Add site-specific custom roles (these just apply styling)
    add_role(app, 'hidden')
    add_role(app, 'applies-to')
    add_role(app, 'object', parent=roles.code_role)
    add_role(app, 'attribute', parent=roles.code_role)
    add_role(app, 'keyword', parent=roles.code_role)
    add_role(app, 'type', parent=roles.code_role)
    add_role(app, 'string', parent=roles.code_role)
    add_role(app, 'path', parent=roles.code_role)
    add_role(app, 'glob', parent=roles.code_role)
    add_role(app, 'var', parent=roles.code_role)
    add_role(app, 'env', parent=roles.code_role)
