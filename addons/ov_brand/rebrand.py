"""Replace the publisher's product name with ours in the texts users see (T2.6).

Upstream writes its product name in thousands of translatable texts: labels,
help texts, error messages, e-mails and their translations. The module does
not copy them; it rewrites the name where the texts are read:

- Python code translations (``_()``, ``env._()``): ``get_translation``;
- web client translations (``_t``): ``ir.http._get_translations_for_webclient``;
- field labels, help texts and selections: ``ir.model.fields``;
- views and QWeb templates: ``ir.ui.view._get_combined_archs``;
- records with application texts (actions, menus, groups, modules): ``_read_format``.

The texts keep the publisher's name where it names the publisher or one of its
other products: the company (Odoo S.A.), the paid edition, Studio, Odoo.sh,
Odoo Online, its versions (Odoo 18) and its mail plugins (Odoo for Gmail).
"""
import ast
import functools
import re
import threading

from markupsafe import Markup, escape

UPSTREAM_NAME = 'Odoo'

# The upstream name, alone or as the name of its bot, with the suffix Turkish
# writes after an apostrophe. Not inside a word, a path or a dotted name.
NAME_RE = re.compile(
    r"(?<![\w./])Odoo(?P<bot>[Bb]ot)?"
    r"(?!\w|\.\w|\s+(?:S\.?A\b|Enterprise|Entreprise|Kurumsal|Studio|Online|v?\d|for\s+(?:Gmail|Outlook)))"
    r"(?:(?P<apostrophe>['’])(?P<suffix>[^\W\d_]+))?",
)
# Addresses given as examples: "odoo@example.com", "jobs@example.odoo.com",
# "notification@odoo.com", "https://www.odoo.com"
EXAMPLE_RES = (
    (re.compile(r"(?<=@)(?:example\.)?odoo\.com\b"), 'example.com'),
    (re.compile(r"(?<![\w.@-])odoo(?=@[\w-]+\.)"), 'info'),
    (re.compile(r"\b(https?://)www\.odoo\.com\b(?![/\w.-])"), r'\1www.example.com'),
    (re.compile(r"(?<=[\"'“])odoo\.com(?=[\"'”])"), 'example.com'),
    (re.compile(r"\b(your|my)company\.odoo\.com\b"), r'\1company.example.com'),
)
# Sentences sending users to the publisher's support desk, which does not
# serve our customers
SUPPORT_RE = re.compile(r"\s*[^.!?\n<>]*(?<![\w.-])(?:https?://)?(?:www\.)?odoo\.com/help\b[^.!?\n<>]*[.!?]?")
# Links to the publisher's home page, in HTML sources: their text is kept
PUBLISHER_LINK_RE = re.compile(
    r"""<a\s[^>]*?\bhref=(["'])https?://(?:www\.)?odoo\.com/?\1[^>]*>(.*?)</a>""", re.DOTALL)
HINT_RE = re.compile(r"Odoo|odoo(?:@|\.com)")

_VOWELS = 'aeıioöuü'
_BACK_VOWELS = 'aıou'
_ROUNDED_VOWELS = 'oöuü'
_VOICELESS = 'çfhkpsşt'


def _tr_lower(text):
    return text.replace('I', 'ı').replace('İ', 'i').lower()


def adapt_tr_suffix(suffix, word, brand):
    """Return the Turkish ``suffix`` written after ``word``, adapted to ``brand``.

    Turkish suffixes follow the last vowel (vowel harmony) and the last sound of
    the word: "Odoo'da", "Odoo'nun", "Odoo'ya" but "Nexus'ta", "Nexus'un",
    "Nexus'a". The suffix is rewritten from its archiphonemes: the two-way
    (a/e) and four-way (i/u) vowels, d/t and c/ç at its start, and the buffer
    consonants y, n and s.
    """
    word_letters = [c for c in _tr_lower(word) if c.isalpha()]
    brand_letters = [c for c in _tr_lower(brand) if c.isalpha()]
    vowel = next((c for c in reversed(brand_letters) if c in _VOWELS), None)
    if not word_letters or not vowel or not suffix.islower():
        return suffix
    last = brand_letters[-1]
    word_vowel_end = word_letters[-1] in _VOWELS
    brand_vowel_end = last in _VOWELS

    if word_vowel_end and not brand_vowel_end:
        # drop the buffer consonant: -yA, -yI, -ylA, -nIn, -sI
        if re.match(r'y|n[ıiuü]n|s[ıiuü](?!z)', suffix):
            suffix = suffix[1:]
    elif not word_vowel_end and brand_vowel_end:
        if re.match(r'[ıiuü]n(?:$|ki)', suffix):  # genitive
            suffix = 'n' + suffix
        elif re.match(r'[aeıiuü]|l[ae](?!r)', suffix):  # dative, accusative, -ylA
            suffix = 'y' + suffix

    out = []
    previous = vowel
    for index, char in enumerate(suffix):
        if index == 0 and char in 'dt':
            char = 't' if last in _VOICELESS else 'd'
        elif index == 0 and char in 'cç':
            char = 'ç' if last in _VOICELESS else 'c'
        elif char == 'i' and index >= 2 and suffix[index - 1] == 'k' and suffix[index - 2] in 'aen':
            pass  # -ki does not follow the vowel harmony
        elif char in 'ae':
            char = 'a' if previous in _BACK_VOWELS else 'e'
        elif char in 'ıiuü':
            back, rounded = previous in _BACK_VOWELS, previous in _ROUNDED_VOWELS
            char = ('u' if rounded else 'ı') if back else ('ü' if rounded else 'i')
        if char in _VOWELS:
            previous = char
        out.append(char)
    return ''.join(out)


def rebrand(text, brand, lang=None):
    """Return ``text`` with the product name ``brand`` in place of the upstream one.

    :param text: a text, HTML markup (``Markup``) included
    :param brand: the product name users see
    :param lang: language of the text; Turkish suffixes are adapted to the brand
    """
    if not text or not brand or not HINT_RE.search(text):
        return text
    is_markup = isinstance(text, Markup)
    name = escape(brand) if is_markup else brand
    turkish = bool(lang) and lang.split('_')[0] == 'tr'

    def replace(match):
        suffix = match['suffix']
        if suffix is None:
            return name
        if turkish:
            suffix = adapt_tr_suffix(suffix, UPSTREAM_NAME + (match['bot'] or ''), brand)
        return f"{name}{match['apostrophe']}{suffix}"

    result = NAME_RE.sub(replace, str(text))
    for pattern, replacement in EXAMPLE_RES:
        result = pattern.sub(replacement, result)
    if not is_markup:
        without_support = SUPPORT_RE.sub('', result)
        if without_support.strip():
            result = without_support
    return Markup(result) if is_markup else result


def rebrand_html(text, brand, lang=None):
    """Rebrand an HTML source, a template's body for instance, and unlink the
    links to the publisher's home page."""
    if not text or not HINT_RE.search(text):
        return text
    unlinked = PUBLISHER_LINK_RE.sub(r'\2', str(text))
    return rebrand(Markup(unlinked) if isinstance(text, Markup) else unlinked, brand, lang)


# Element attributes users see in views and templates
VISIBLE_ATTRIBUTES = frozenset({
    'alt', 'aria-label', 'confirm', 'content', 'data-tooltip', 'help', 'label',
    'placeholder', 'string', 'sum', 'title',
})


def is_code(node):
    """Return whether the text in ``node`` is code: scripts and styles."""
    return node is not None and node.tag in ('script', 'style')


def rebrand_arch(arch, brand, lang=None):
    """Rebrand, in place, the texts and visible attributes of a view's etree.

    Expressions (``t-*`` attributes, ``invisible``...) are left as they are.
    """
    for node in arch.iter():
        if node.tail and not is_code(node.getparent()):
            node.tail = rebrand(node.tail, brand, lang)
        if not isinstance(node.tag, str):  # comments, processing instructions
            continue
        if node.text and not is_code(node):
            node.text = rebrand(node.text, brand, lang)
        for attribute in VISIBLE_ATTRIBUTES.intersection(node.attrib):
            node.set(attribute, rebrand(node.get(attribute), brand, lang))
    return arch


# Code terms of a translation template: the msgid of the entries marked
# odoo-javascript or odoo-python, on one or several lines
_POT_CODE_ENTRY_RE = re.compile(
    r'^#\. (odoo-javascript|odoo-python)\n(?:#.*\n)*(?:msgctxt .*\n)?msgid ((?:".*"\n)+)', re.MULTILINE)


@functools.cache
def _pot_code_sources(module):
    from odoo.tools.misc import file_open  # noqa: PLC0415

    try:
        with file_open(f'{module}/i18n/{module}.pot') as pot:
            content = pot.read()
    except (OSError, ValueError):
        return {}
    sources = {}
    for match in _POT_CODE_ENTRY_RE.finditer(content):
        kind, lines = match.groups()
        if HINT_RE.search(lines):
            source = ''.join(ast.literal_eval(line) for line in lines.splitlines())
            sources.setdefault(kind, set()).add(source)
    return {kind: frozenset(kind_sources) for kind, kind_sources in sources.items()}


def code_sources(module, kind='odoo-javascript'):
    """Return the source texts of the code terms of ``module`` naming the
    upstream product, from the module's translation template.

    The web client gets the translated terms only; the terms without a
    translation, all of them in English, are added from here.

    :param kind: ``odoo-javascript`` (web client) or ``odoo-python``
    """
    return _pot_code_sources(module).get(kind, frozenset())


# Product name of each database having this module, for the code translations,
# which are not given an environment. Filled by tools.get_brand_name(), which
# the web client and every QWeb rendering call.
_brands = {}


def set_database_brand(dbname, brand):
    _brands[dbname] = brand


def forget_database(dbname):
    _brands.pop(dbname, None)


def current_brand():
    """Return the product name of the current thread's database, None without this module."""
    dbname = getattr(threading.current_thread(), 'dbname', None)
    return _brands.get(dbname) if dbname else None


def patch_code_translations():
    """Rebrand the code translations returned by ``get_translation``.

    The function is the single entry point of ``_()``, ``env._()`` and lazy
    translations. It is imported by name in ``odoo.orm.environments``.
    """
    from odoo.orm import environments  # noqa: PLC0415
    from odoo.tools import translate  # noqa: PLC0415

    original = translate.get_translation
    if getattr(original, 'ov_brand_patched', False):
        return

    @functools.wraps(original)
    def get_translation(module, lang, source, args):
        result = original(module, lang, source, args)
        if isinstance(result, str) and HINT_RE.search(result):
            brand = current_brand()
            if brand:
                result = rebrand(result, brand, lang)
        return result

    get_translation.ov_brand_patched = True
    translate.get_translation = get_translation
    environments.get_translation = get_translation
