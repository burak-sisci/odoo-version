"""Validation rules of tools/po_coverage.py (python -m unittest discover -s tools/tests)."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from po_coverage import problems, underline_problems  # noqa: E402


class TestProblems(unittest.TestCase):

    def assertAccepted(self, msgid, msgstr):
        self.assertEqual(problems(msgid, msgstr), [])

    def assertRejected(self, msgid, msgstr, problem):
        found = problems(msgid, msgstr)
        self.assertTrue(any(problem in p for p in found), found)

    def test_empty(self):
        self.assertRejected("Draft", " ", "empty translation")

    def test_printf(self):
        self.assertAccepted("%(a)s of %(b)s", "%(b)s içinde %(a)s")
        self.assertRejected("%(a)s of %(b)s", "%(a)s içinde", "named placeholders")
        self.assertAccepted("%s at %d", "%s, %d")
        self.assertRejected("%s at %d", "%d, %s", "positional placeholders")
        # percentages are not placeholders
        self.assertAccepted("CA State 6%", "CA Eyalet %6")

    def test_format_placeholders(self):
        self.assertAccepted("{name} is late", "{name} gecikti")
        self.assertRejected("{name} is late", "{ad} gecikti", "{placeholders}")

    def test_expressions(self):
        msgid = "{{ object.name }} {{ object.state in ('draft', 'sent') and 'Quotation' or 'Order' }}"
        # the strings the expression outputs may be translated, its spacing may differ
        self.assertAccepted(msgid, "{{object.name}} {{ object.state in ('draft','sent') and 'Teklif' or 'Sipariş'}}")
        self.assertAccepted("{{ 'Paid' if object.paid else 'Due' }}", "{{ 'Ödendi' if object.paid else 'Vadeli' }}")
        # the compared values, the fields and the expressions stay
        for msgstr in (
            "{{ object.name }} {{ object.state in ('taslak', 'sent') and 'Teklif' or 'Sipariş' }}",
            "{{ object.ref }} {{ object.state in ('draft', 'sent') and 'Teklif' or 'Sipariş' }}",
            "{{ object.name }}",
            "{{ object.name }} {{ object.state in ('draft', 'sent') and 'Teklif' or 'Sipariş }}",
        ):
            with self.subTest(msgstr=msgstr):
                self.assertRejected(msgid, msgstr, "{placeholders}")
        self.assertRejected("{{ 'Paid' if object.paid else 'Due' }}", "{{ 'Ödendi' if object.due else 'Vadeli' }}", "{placeholders}")

    def test_tags(self):
        msgid = '<span class="o_stat_text" invisible="not count">Items</span>'
        self.assertAccepted(msgid, '<span class="o_stat_text" invisible="not count">Kalemler</span>')
        self.assertRejected(msgid, '<span class="o_stat_text">Kalemler</span>', "tags")
        self.assertRejected(msgid, "Kalemler", "tags")
        # translated attributes may change, the order of the tags too
        self.assertAccepted('<i title="Edit"/> <b>Save</b>', '<b>Kaydet</b> <i title="Düzenle"/>')

    def test_line_breaks(self):
        self.assertAccepted("\nText\n", "\nMetin\n")
        self.assertRejected("\nText", "Metin", "leading line break")
        self.assertRejected("Text", "Metin\n", "trailing line break")

    def test_product_name(self):
        self.assertAccepted("Odoo allows it", "Odoo buna izin verir")
        self.assertRejected("It is allowed", "Odoo buna izin verir", "product name added")

    def test_title_underline(self):
        self.assertAccepted("Title\n=====\n", "Başlık\n======\n")
        self.assertRejected("Title\n=====\n", "Uzun Başlık\n=====\n", "title underline")

    def test_title_underline_alone(self):
        # also applied to upstream description translations, whose other problems are not checked
        self.assertEqual(underline_problems("\nBaşlık\n======\n\nMetin\n"), [])
        # upstream 'account': a trailing space made the title one longer than its underline
        self.assertTrue(underline_problems("\nFaturalama ve Ödemeler \n======================\n"))
        self.assertEqual(underline_problems("a\n---\nb\n------\n"), [])


if __name__ == "__main__":
    unittest.main()
