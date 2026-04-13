import bleach
import markdown
from django.utils.safestring import mark_safe

_ALLOWED_TAGS = frozenset(
    [
        'p',
        'pre',
        'code',
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',
        'ul',
        'ol',
        'li',
        'blockquote',
        'a',
        'strong',
        'em',
        'table',
        'thead',
        'tbody',
        'tr',
        'th',
        'td',
        'hr',
        'br',
    ]
)
_ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'rel'],
    'code': ['class'],
    'pre': ['class'],
    'th': ['align'],
    'td': ['align'],
}


def render_markdown(text: str) -> str:
    if not text:
        return ''
    raw = markdown.markdown(
        text,
        extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.nl2br',
        ],
    )
    clean = bleach.clean(
        raw,
        tags=_ALLOWED_TAGS,
        attributes=_ALLOWED_ATTRIBUTES,
        strip=True,
    )
    return mark_safe(clean)
