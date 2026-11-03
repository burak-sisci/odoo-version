"""Checks for the Turkish names of accounts, taxes, tax groups and fiscal positions.

Used by the tests of this module. The rules come from the errors found in the
upstream Turkish chart of accounts (docs/research/l10n-tr.md, T3.1): English
names left untranslated, English abbreviations, machine translations, and
capitals written with the rules of English instead of Turkish.
"""
import re

# English abbreviations of the upstream names ("WH 20% (2/10)", "0% EX").
ENGLISH_ABBREVIATIONS = re.compile(r'\b(?:WH|EX|PR|ST|VAT|SSI)\b')

# Machine translations seen in the upstream data: "WH" read as "when", and an
# imperative instead of a noun.
FORBIDDEN_PHRASES = (
    re.compile(r'\bne zaman\b', re.IGNORECASE),
    re.compile(r'\bsatın al\b', re.IGNORECASE),
)

# Typos and leftovers of the upstream data.
TYPOS = (
    re.compile(r'\bYE\b'),  # "SATIŞ YE DAĞITIM" for "SATIŞ VE DAĞITIM"
    re.compile(r'\(\d\)$'),  # footnote marker at the end: "FAZLALARI(1)"
)

FRONT_VOWELS = set('EİÖÜ')
VOWELS = set('AIOUÂÛEİÖÜ')

# Words whose dotted "İ" a non-Turkish upper-case conversion turns into "I"
# without breaking the vowel harmony of the word. The harmony rule below
# finds the other cases.
WRONG_ROOTS = (
    'TAHSIL', 'TASDIK', 'FAIZ', 'KAMBIYO', 'FINANS', 'KIRALAMA', 'HAKEDIŞ',
    'DIĞER', 'İŞCİLİK', 'DÜŞÜKLÜGÜ', 'MAMÜL',
)


def _is_upper_word(word):
    letters = [c for c in word if c.isalpha()]
    return len(letters) >= 2 and all(c.isupper() for c in letters)


def upper_case_problems(text):
    """Return the upper-case words of ``text`` that break the Turkish rules.

    In a Turkish suffix the vowel follows the vowel before it: after a front
    vowel (E, İ, Ö, Ü) comes "İ", never "I". A word like "EDILMEYEN" therefore
    comes from an English upper-case conversion of "edilmeyen".
    """
    problems = []
    for word in re.findall(r'[^\W\d_]+', text):
        if not _is_upper_word(word):
            continue
        last_vowel = None
        for char in word:
            if char == 'I' and last_vowel in FRONT_VOWELS:
                problems.append(word)
                break
            if char in VOWELS:
                last_vowel = char
        else:
            if any(root in word for root in WRONG_ROOTS):
                problems.append(word)
    return problems


def name_problems(text, english=None):
    """Return the problems found in a Turkish name, as short descriptions.

    :param text: the name shown to a Turkish user
    :param english: the English name of the same record, if any
    """
    if not text:
        return ['empty name']
    problems = []
    if english and text == english and re.search(r'[A-Za-z]{2,}', text):
        problems.append('English name')
    problems += [f'English abbreviation "{m}"' for m in ENGLISH_ABBREVIATIONS.findall(text)]
    problems += [f'machine translation "{p.search(text)[0]}"' for p in FORBIDDEN_PHRASES if p.search(text)]
    problems += [f'typo "{p.search(text)[0]}"' for p in TYPOS if p.search(text)]
    problems += [f'upper case "{word}"' for word in upper_case_problems(text)]
    return problems
