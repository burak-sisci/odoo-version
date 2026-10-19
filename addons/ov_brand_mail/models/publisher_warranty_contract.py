from odoo import api, models


class PublisherWarrantyContract(models.AbstractModel):
    _inherit = 'publisher_warranty.contract'

    @api.model
    def _get_sys_logs(self):
        """Never send the report: it carries the database identifier, user
        counts, installed apps and the company's name, e-mail and phone (KVKK).
        An empty answer leaves the database as it is."""
        return {'messages': []}
