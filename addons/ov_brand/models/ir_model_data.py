from odoo import api, models


class IrModelData(models.Model):
    _inherit = 'ir.model.data'

    @api.model
    def _process_end(self, modules):
        # Called once all the modules of an installation or upgrade are loaded,
        # just before the modules marked for removal are removed. Removing the
        # online service modules here also undoes the ones installed from the
        # command line, together with the modules they brought.
        res = super()._process_end(modules)
        self.env['ir.module.module']._ov_remove_online_services()
        return res
