from odoo import models
from odoo.tools import get_lang

from odoo.addons.ov_l10n_tr.tools import turkish_capitalize

try:
    from num2words import num2words
except ImportError:
    num2words = None


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    def amount_to_text(self, amount):
        """Write the amount in Turkish words the way Turkish documents do.

        - Numbers in words are written as one word in money matters (TDK
          spelling rules): 'binikiyüzotuzdört'.
        - The first letter follows the Turkish rule: 'İkibin', not 'Ikibin'.
        - Unit and subunit follow each other without 've':
          'Binikiyüzotuzdört Türk Lirası Ellialtı Kuruş'.
        """
        self.ensure_one()
        if num2words is None or get_lang(self.env).iso_code.split('_')[0] != 'tr':
            return super().amount_to_text(amount)
        integral, _sep, fractional = f"{amount:.{self.decimal_places}f}".partition('.')
        parts = [turkish_capitalize(num2words(int(integral), lang='tr')), self.currency_unit_label or self.name]
        if int(fractional or 0):
            parts += [turkish_capitalize(num2words(int(fractional), lang='tr')), self.currency_subunit_label]
        return ' '.join(part for part in parts if part)
