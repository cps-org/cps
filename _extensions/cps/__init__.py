import os
import re
from dataclasses import dataclass
from types import NoneType
from typing import cast

from docutils import nodes
from docutils.parsers.rst import Directive, directives, roles
from docutils.transforms import Transform

import jsb

from sphinx import addnodes, domains
from sphinx.util import logging
from sphinx.util.docutils import SphinxRole
from sphinx.util.nodes import clean_astext

logger = logging.getLogger(__name__)

# =============================================================================
def simplify_text(node):
    paragraphs = []
    for p in clean_astext(node).split('\n\n'):
        paragraphs.append(p.replace('\n', ' '))

    return '\n\n'.join(paragraphs)

# =============================================================================
def make_code(text, classname):
    return nodes.literal(text, text, classes=['code', classname])

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

            refuri = ref['refuri'] if 'refuri' in ref else None
            if refuri and refuri.startswith('./'):
                continue

            # Convert remaining non-external links to intra-document references
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
class ObjectDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    has_content = True

    # -------------------------------------------------------------------------
    def run(self):
        name = self.arguments[0]

        # Create section node
        section = nodes.section()
        section.document = self.state.document
        section.line = self.lineno
        section['names'].append(f'{name}(object)')

        # Create text nodes for section title
        title = [
            make_code(name, 'object'),
            nodes.inline('(object)', '(object)', classes=['hidden']),
        ]
        section += nodes.title(name, '', *title)

        # Parse object description
        content = nodes.Element()
        self.state.nested_parse(self.content, self.content_offset, content)
        section += content.children

        # Record section reference
        self.state.document.note_implicit_target(section, section)

        # Record object on domain
        env = self.state.document.settings.env
        domain = cast(CpsDomain, env.get_domain('cps'))
        domain.note_object(name, simplify_text(content))

        # Return generated nodes
        return [section]

# =============================================================================
class AttributeDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    has_content = True
    option_spec = {
        'type': directives.unchanged,
        'context': lambda a: a.split(),
        'overload': directives.flag,
        'required': directives.flag,
        'conditionally-required': directives.flag,
    }

    # -------------------------------------------------------------------------
    def make_field(self, name, rawtext, body):
        src, srcline = self.state.state_machine.get_source_and_line()

        field = nodes.field()
        field.source = src
        field.line = srcline

        field += nodes.field_name(name, name)
        field += nodes.field_body(rawtext, *body)

        return field

    # -------------------------------------------------------------------------
    def make_list(self, values, nodetype, classes):
        content = [nodetype(values[0], values[0], classes=classes)]
        for value in values[1:]:
            content += [
                nodes.Text(', '),
                nodetype(value, value, classes=classes),
            ]
        return content

    # -------------------------------------------------------------------------
    def parse_type(self, typedesc):
        if '|' in typedesc:
            types = typedesc.split('|')
            content = self.parse_type(types[0])
            for t in types[1:]:
                content += [
                    nodes.Text(' '),
                    nodes.inline('or', 'or', classes=['separator']),
                    nodes.Text(' '),
                ] + self.parse_type(t)

            return content

        outer, inner = jsb.decompose_typedesc(typedesc)
        if outer:
            content = [
                make_code(outer, 'type'),
                nodes.Text(' of '),
            ]
            if outer == 'map':
                content += [
                    make_code('string', 'type'),
                    nodes.Text(' to '),
                ]

            return content + self.parse_type(inner)

        elif typedesc in jsb.BUILTIN_TYPES:
            return [make_code(typedesc, 'type')]

        else:
            return [make_code(typedesc, 'object')]

    # -------------------------------------------------------------------------
    def run(self):
        name = self.arguments[0]
        typedesc = self.options['type']
        context = self.options['context']
        overload = 'overload' in self.options
        required = 'required' in self.options
        conditionally_required = 'conditionally-required' in self.options

        if overload:
            target = f'{name} ({context[0]})'
        else:
            target = name

        if required:
            required_text = 'Yes'
        elif conditionally_required:
            required_text = 'Special'
        else:
            required_text = 'No'

        # Create section node
        section = nodes.section()
        section.document = self.state.document
        section.line = self.lineno
        section['names'].append(target)

        # Create text nodes for section title
        title = [make_code(name, 'attribute')]
        if overload:
            title += [
                nodes.Text(' '),
                nodes.inline(f'({context[0]})', f'({context[0]})',
                             classes=['applies-to']),
            ]
        section += nodes.title(target, '', *title)

        # Create nodes for attribute information
        fields = nodes.field_list()
        fields += self.make_field(
            'Type', typedesc, self.parse_type(typedesc))
        fields += self.make_field(
            'Applies To', ', '.join(context),
            self.make_list(context, nodes.literal, ['code', 'object']))
        fields += self.make_field(
            'Required', required_text, [nodes.Text(required_text)])
        section += fields

        # Parse attribute description
        content = nodes.Element()
        self.state.nested_parse(self.content, self.content_offset, content)
        section += content.children

        # Record section reference
        self.state.document.note_implicit_target(section, section)

        # Record object on domain
        env = self.state.document.settings.env
        domain = cast(CpsDomain, env.get_domain('cps'))
        domain.note_attribute(name, context, typedesc, required=required,
                              description=simplify_text(content), node=section)

        # Return generated nodes
        return [section]

# =============================================================================
class SchemaRole(SphinxRole):
    def run(self):
        uri = f'./{self.config.schema_filename}'
        node = nodes.reference(self.rawtext, self.text, refuri=uri)
        return [node], []

# =============================================================================
@dataclass
class Attribute:
    typedesc: str
    description: str
    required: bool

# =============================================================================
class AttributeSet:

    # -------------------------------------------------------------------------
    def __init__(self, name, context, attribute, node):
        self.name = name
        self.instances = [attribute]
        self.context = {c: (0, node) for c in context}

    # -------------------------------------------------------------------------
    def overload(self, context, attribute, node):
        i = len(self.instances)
        self.instances.append(attribute)
        for c in context:
            if c in self.context:
                logger.warning('duplicate declaration of attribute '
                               f'{self.name!r} on object {c!r}',
                               location=node)
                logger.warning(f'{self.name!r} was previously declared here',
                               location=self.context[c][1])
            else:
                self.context[c] = (i, node)

# =============================================================================
class CpsDomain(domains.Domain):
    name = 'cps'

    # -------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Site-specific directives (used for JSON schema generation)
        self.directives['object'] = ObjectDirective
        self.directives['attribute'] = AttributeDirective

        # Site-specific roles
        self.roles['schema'] = SchemaRole()

        # Additional site-specific roles (these just apply styling)
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
    @property
    def objects(self):
        return self.data.setdefault('objects', {})

    # -------------------------------------------------------------------------
    @property
    def attributes(self):
        return self.data.setdefault('attributes', {})

    # -------------------------------------------------------------------------
    def note_object(self, name, description):
        if name not in self.objects:
            self.objects[name] = description

    # -------------------------------------------------------------------------
    def note_attribute(self, name, context, typedesc,
                       required, description, node):
        a = Attribute(typedesc, description, required)
        if name not in self.attributes:
            self.attributes[name] = AttributeSet(name, context, a, node)
        else:
            self.attributes[name].overload(context, a, node)

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
def write_schema(app, exception):
    if exception is not None:
        return

    config = app.env.config
    title = f'{config.project} v{config.version}'

    domain = cast(CpsDomain, app.env.get_domain('cps'))
    schema = jsb.JsonSchema(title, config.schema_id)

    object_attributes = {}
    for attribute_set in domain.attributes.values():
        for i, attribute in enumerate(attribute_set.instances):
            schema.add_attribute(
                attribute_set.name, i,
                attribute.typedesc,
                attribute.description,
            )

        for context, attribute_ref in attribute_set.context.items():
            attribute = (
                attribute_set.name,
                attribute_ref[0],
                attribute_set.instances[attribute_ref[0]].required
            )
            if context in object_attributes:
                object_attributes[context].append(attribute)
            else:
                object_attributes[context] = [attribute]

    for name, description in domain.objects.items():
        schema.add_object_type(name, description, object_attributes[name])

    output_path = os.path.join(app.outdir, config.schema_filename)
    schema.write(config.schema_root_object, output_path, config.schema_indent)

# =============================================================================
def setup(app):
    app.add_domain(CpsDomain)
    app.add_config_value('schema_id', '', '', [str])
    app.add_config_value('schema_filename', 'schema.json', '', [str])
    app.add_config_value('schema_root_object', None, '', [str])
    app.add_config_value('schema_indent', None, '', [NoneType, int])

    # Add custom transform to resolve cross-file references
    app.add_transform(InternalizeLinks)

    # Add hook to write machine-readable schema description on completion
    app.connect('build-finished', write_schema)
