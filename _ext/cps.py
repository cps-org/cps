from sphinx import domains
from docutils.parsers.rst import directives, roles

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
    del app.domains['std'].roles['keyword']

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
