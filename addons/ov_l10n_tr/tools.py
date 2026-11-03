"""Turkish identifiers (tax number VKN, citizen number TCKN, MERSIS number) and place names."""
import re

from stdnum.exceptions import InvalidFormat, InvalidLength

TURKEY = 'TR'
VKN = 'VKN'  # tax number of a legal entity, 10 digits
TCKN = 'TCKN'  # citizen number of a natural person, 11 digits
MERSIS_LENGTH = 16
# Name of the central district of the 51 provinces without a metropolitan municipality.
CENTRAL_DISTRICT = 'Merkez'
NON_DIGITS = re.compile(r'\D')
# Digits, with the separators people type between groups.
DIGITS_AND_SEPARATORS = re.compile(r'[\d\s.-]+')
SPACES = re.compile(r'\s+')
CIRCUMFLEX = str.maketrans('âîû', 'aiu')


def fold_name(name):
    """Key to compare Turkish place names typed by people: 'KADIKÖY ' and 'Kadıköy' match.

    Turkish case rules (I/ı, İ/i), no circumflex (the official names have none:
    'Balâ' is 'Bala'), single spaces.
    """
    name = (name or '').replace('I', 'ı').replace('İ', 'i').lower().translate(CIRCUMFLEX)
    return SPACES.sub(' ', name).strip()


def tax_id_type(vat):
    """Return VKN or TCKN after the number of digits of a Turkish tax ID, '' otherwise.

    The checksum is left to the VAT check of the partner, which runs on save.
    """
    digits = NON_DIGITS.sub('', vat or '')
    return {10: VKN, 11: TCKN}.get(len(digits), '')


def mersis_validate(value):
    """Normalize a MERSIS number (Central Registry System number, 16 digits).

    Only the length is checked: its inner structure (a leading 0 and the tax
    number for a company, the citizen number for a sole proprietor) is not
    published as a rule.
    """
    value = value.strip()
    if not DIGITS_AND_SEPARATORS.fullmatch(value):
        raise InvalidFormat()
    digits = NON_DIGITS.sub('', value)
    if len(digits) != MERSIS_LENGTH:
        raise InvalidLength()
    return digits
