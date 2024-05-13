import pygments.token

from sphinx.pygments_styles import SphinxStyle

# =============================================================================
class CpsDataStyle(SphinxStyle):
    background_color = ''

    styles = SphinxStyle.styles
    styles.update({
        pygments.token.Name.Tag:                '#15a',
        pygments.token.Literal.String.Double:   '#d32',
    })
