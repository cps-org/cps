import re

from docutils import nodes
from docutils.parsers.rst import directives, roles
from docutils.transforms import Transform

from sphinx import addnodes, domains

# =============================================================================
class InternalizeLinks(Transform):
    default_priority = 200

    # -------------------------------------------------------------------------
    def is_internal_link(self, refuri):
        if not refuri:
            return True

        if '://' in refuri or 'mailto:' in refuri:
            return False

        return True

    # -------------------------------------------------------------------------
    def apply(self, **kwargs):
        for ref in self.document.findall(nodes.reference):
            # Skip inter-document links
            if 'refname' in ref:
                if self.document.nameids.get(ref['refname']):
                    continue

            # Convert remaining non-external links to intra-document references
            refuri = ref['refuri'] if 'refuri' in ref else None
            if self.is_internal_link(refuri):
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

# =============================================================================
class CpsDomain(domains.Domain):
    name = 'cps'

    # -------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Site-specific custom roles (these just apply styling)
        self.add_role('hidden')
        self.add_role('applies-to')
        self.add_role('separator')
        self.add_code_role('object')
        self.add_code_role('attribute')
        self.add_code_role('feature')
        self.add_code_role('feature.opt', styles=['feature', 'optional'])
        self.add_code_role('feature.var', styles=['feature', 'var'])
        self.add_code_role('keyword')
        self.add_code_role('type')
        self.add_code_role('string')
        self.add_code_role('path')
        self.add_code_role('glob')
        self.add_code_role('var')
        self.add_code_role('env')

    # -------------------------------------------------------------------------
    def add_role(self, name, styles=None, parent=roles.generic_custom_role):
        options = {}
        if styles is None:
            styles = name
        else:
            styles = ' '.join([name] + styles)

        options['class'] = directives.class_option(styles)
        self.roles[name] = roles.CustomRole(name, parent, options)

    # -------------------------------------------------------------------------
    def add_code_role(self, name, styles=None, parent=roles.code_role):
        self.add_role(name, styles, parent)

# =============================================================================
def setup(app):
    app.add_domain(CpsDomain)

    # Add custom transform to resolve cross-file references
    app.add_transform(InternalizeLinks)
