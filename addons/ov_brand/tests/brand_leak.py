"""Brand leak test (T2.6): what a leak is, and the texts the test accepts.

A leak is the upstream product name, in any case, or a link to the
publisher's site or logos, in a text users see. ALLOWLIST lists the accepted
ones with the reason.

Each entry is ``(surface, key, reason)``; ``key`` is a shell pattern
(``fnmatch``) matched against the key the test reports. Surfaces:

- ``python``, ``web``: code terms, key ``<module>:<source>``;
- ``field``: key ``<model>.<field>.<attribute>``;
- ``view``: views and QWeb templates, key ``<xml id>``;
- ``record``: key ``<model>:<xml id>.<field>``;
- ``mail_template``: key ``<xml id>.<field>`` (ov_brand_mail);
- ``page``: key ``<url path>``.

The names of the publisher (Odoo S.A.) and of its other products (the paid
edition, Studio, Odoo.sh, Odoo Online, the mail plugins, its versions) are
accepted everywhere; rebrand.NAME_RE keeps them.
"""
import re
from fnmatch import fnmatchcase

from odoo.addons.ov_brand.rebrand import VISIBLE_ATTRIBUTES, is_code

ALLOWLIST = [
    # Technical names: spreadsheet formulas and the variable of the MCP key
    # example. Formula names are not shown in Community, where spreadsheets
    # only open as read-only dashboards; NEXUS.* aliases come with spreadsheet
    # editing, the ODOO.* names stay for saved spreadsheets (K13).
    ('web', 'spreadsheet*:*ODOO.*', "Formula names of the spreadsheets (K13)"),
    ('python', 'spreadsheet*:*ODOO.*', "Formula names of the spreadsheets (K13)"),
    ('view', 'base.form_res_users_key_show', "Name of an environment variable in a code example"),
    # The paid modules and providers are not listed (remove_odoo_enterprise)
    ('view', 'base.module_form', "Pricing link of the paid modules, which are not listed"),
    ('view', 'base.module_view_kanban', "Pricing link of the paid modules, which are not listed"),
    ('view', 'payment.payment_provider_form', "Pricing link of the paid providers, which are not listed"),
    ('view', 'payment.payment_provider_kanban', "Pricing link of the paid providers, which are not listed"),
    ('record', 'ir.module.module:*remove_odoo_enterprise.shortdesc', "Name of the module hiding the paid edition"),
    ('python', 'base_import_module:*pricing-plan*',
     "Pricing link of the paid edition in an error of the module import, which administrators see"),
    ('field', 'ir.module.module.total_lines_of_code.help',
     "Pricing note of the paid edition; the field is in no view"),
    # Legal names
    ('field', 'ir.module.module.license.selection', "Names of the licenses of the modules"),
    # Placeholders replaced when rendered
    ('view', 'account.report_statement', "Placeholder of the bank's owner, replaced by the partner name"),
    # Not rendered: the digest drops the section (ov_brand_digest, T2.5)
    ('view', 'digest.digest_section_mobile', "Section of the digest that is not rendered"),
    # Our own templates comparing with the upstream default
    ('view', 'web.login', "Expression of ov_brand comparing the page title with the upstream default"),
    # Developer tools
    ('view', 'web.view_speedscope_index', "Profiler page of the developer mode"),
]

LANGS = ('en_US', 'tr_TR')
# The upstream name as a word, in any case
LEAK_RE = re.compile(r"(?<![\w/-])odoo(?![\w-])", re.IGNORECASE)
# Names of the publisher and of its other products (rebrand.NAME_RE)
KEPT_RE = re.compile(
    r"Odoo(?:\.sh\b|\s+(?:S\.?A\b|Enterprise|Entreprise|Kurumsal|Studio|Online|v?\d|for\s+(?:Gmail|Outlook)))")
# Links to the publisher's site and its logos
LINK_RE = re.compile(r"odoo\.com|odoo[\w-]*\.(?:svg|png|jpe?g|gif|ico)\b", re.IGNORECASE)
LINK_ATTRIBUTES = ('href', 'src', 'action', 't-att-href', 't-attf-href', 't-att-src', 't-attf-src')
# Literal texts in template expressions
EXPRESSION_RE = re.compile(r"""(['"])[^'"\n]*\bOdoo\b[^'"\n]*\1""")


def find_leak(text):
    """Return the first leak of ``text``: the upstream name outside the kept names."""
    if not text:
        return None
    for match in LEAK_RE.finditer(text):
        if not KEPT_RE.match(text, match.start()):
            return text
    return None


def is_allowed(surface, key):
    return any(entry[0] == surface and fnmatchcase(key, entry[1]) for entry in ALLOWLIST)


def is_leaking_attribute(attribute, value):
    if attribute in VISIBLE_ATTRIBUTES:
        return bool(find_leak(value))
    if attribute in LINK_ATTRIBUTES:
        return bool(LINK_RE.search(value))
    return attribute.startswith('t-') and bool(EXPRESSION_RE.search(value))


def scan_arch(arch):
    """Yield the leaks of a view's etree: texts, visible attributes, links and
    literal texts of expressions."""
    for node in arch.iter():
        element = isinstance(node.tag, str)
        texts = [node.text] if element and not is_code(node) else []
        if not is_code(node.getparent()):
            texts.append(node.tail)
        for text in texts:
            if find_leak(text):
                yield text.strip()
        if not element:
            continue
        for attribute, value in node.attrib.items():
            if is_leaking_attribute(attribute, value):
                yield f'{attribute}="{value}"'
