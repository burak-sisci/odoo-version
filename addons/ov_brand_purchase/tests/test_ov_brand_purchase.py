from odoo.tests import HttpCase, tagged


@tagged('post_install', '-at_install')
class TestOvBrandPurchase(HttpCase):

    def test_portal_purchase_order(self):
        vendor = self.env['res.partner'].create({'name': 'Fictional Vendor', 'email': 'vendor@example.com'})
        product = self.env['product.product'].create({'name': 'Fictional Part'})
        order = self.env['purchase.order'].create({
            'partner_id': vendor.id,
            'order_line': [(0, 0, {'product_id': product.id, 'product_qty': 1, 'price_unit': 10})],
        })
        order.button_confirm()
        response = self.url_open(order.get_portal_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn('portal_connect_software_modal', response.text)
        self.assertIn(f'/my/purchase/{order.id}/download_edi', response.text)
        self.assertNotIn('odoo.com', response.text)
        self.assertNotIn('Not using Odoo', response.text)
