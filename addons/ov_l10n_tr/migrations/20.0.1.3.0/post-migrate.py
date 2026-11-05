from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    # 20.0.1.3.0: Turkish documents write the invoice total in words.
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.company'].search([('chart_template', '=', 'tr')]).display_invoice_amount_total_words = True
