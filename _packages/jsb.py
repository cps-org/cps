import json
import re

BUILTIN_TYPES = {
    'null',
    'string',
}

# =============================================================================
def decompose_typedesc(typedesc):
    m = re.match(r'^(list|map)[(](.*)[)]$', typedesc)
    return m.groups() if m else (None, typedesc)

# =============================================================================
def split_typedesc(typedesc):
    assert typedesc.count('(') == typedesc.count(')')

    types = []
    start = 0
    depth = 0
    for n in range(len(typedesc)):
        if typedesc[n] == '(':
            depth += 1
        elif typedesc[n] == ')':
            assert depth > 0
            depth -= 1
        elif depth == 0 and typedesc[n] == '|':
            types.append(typedesc[start:n])
            start = n + 1

    types.append(typedesc[start:])

    print(f'split typedesc {typedesc!r} => {types!r}')
    return types

# =============================================================================
class JsonSchema:
    # -------------------------------------------------------------------------
    def __init__(self, title, uri):
        self.meta = {
            '$schema': 'http://json-schema.org/draft-07/schema',
            '$id': uri,
            'title': title,
        }
        self.types = {}
        self.object_types = {}
        self.attributes = {}

    # -------------------------------------------------------------------------
    def add_type(self, typedesc):
        if typedesc in self.types:
            # Type already defined; nothing to do
            return

        types = split_typedesc(typedesc)
        if len(types) > 1:
            for t in types:
                self.add_type(t)

            self.types[typedesc] = {
                'oneOf': [
                    {'$ref': f'#/definitions/types/{t}'} for t in types
                ],
            }

            return

        outer, inner = decompose_typedesc(typedesc)
        if outer:
            self.add_type(inner)

            if outer == 'list':
                self.types[typedesc] = {
                    'type': 'array',
                    'items': {'$ref': f'#/definitions/types/{inner}'},
                }

            else:
                self.types[typedesc] = {
                    'type': 'object',
                    'patternProperties': {
                        '': {'$ref': f'#/definitions/types/{inner}'},
                    },
                }

        elif typedesc in BUILTIN_TYPES:
            # Handle simple (non-compound) types
            self.types[typedesc] = {'type': typedesc}

        else:
            # Anything unknown is assumed to be an object type, which must be
            # defined via add_object_type
            pass

    # -------------------------------------------------------------------------
    def add_attribute(self, name, instance, typedesc, typeformat,
                      description, default=None):
        attr = {
            'description': description,
            '$ref': f'#/definitions/types/{typedesc}',
        }

        if typeformat:
            attr['format'] = typeformat

        if default:
            attr['default'] = json.loads(default)

        self.attributes[f'{name}@{instance}'] = attr

        self.add_type(typedesc)

    # -------------------------------------------------------------------------
    def add_object_type(self, name, description, attributes, strict=False):
        self.object_types[name] = {
            'type': 'object',
            'description': description,
            'properties': {
                n: {'$ref': f'#/definitions/attributes/{n}@{i}'}
                for n, i, r in attributes
            },
            'required': [n for n, i, r in attributes if r],
            'additionalProperties': not strict,
        }

    # -------------------------------------------------------------------------
    def _build_schema(self, root_object):
        all_types = self.types
        all_types.update(self.object_types)

        schema = self.meta
        schema['definitions'] = {
            'types': all_types,
            'attributes': self.attributes,
        }
        schema['$ref'] = f'#/definitions/types/{root_object}'

        return schema

    # -------------------------------------------------------------------------
    def write(self, root_object, path, indent=None):
        json.dump(
            self._build_schema(root_object),
            fp=open(path, 'wt'),
            indent=indent,
        )
