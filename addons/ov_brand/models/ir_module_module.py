import logging

from odoo import api, models
from odoo.exceptions import UserError

from odoo.addons.ov_brand.tools import ONLINE_SERVICE_MODULES

_logger = logging.getLogger(__name__)


class IrModuleModule(models.Model):
    _inherit = 'ir.module.module'

    def button_install(self):
        # Only the installations started from the interface come here: the
        # command line marks the modules before the add-ons are loaded. Those
        # are undone at the end of the loading (_ov_remove_online_services).
        online = self.search([('name', 'in', ONLINE_SERVICE_MODULES), ('state', '=', 'uninstalled')])
        res = super().button_install()
        if online.filtered(lambda module: module.state == 'to install'):
            raise UserError(self.env._(
                "These modules need the publisher's online services, which this product does not use: %s",
                ", ".join(self.mapped('shortdesc')),
            ))
        return res

    @api.model
    def _ov_online_service_dependents(self):
        """Return the names of the modules that need an online service
        module, installed or not, the online service modules included."""
        online = self.sudo().search([('name', 'in', ONLINE_SERVICE_MODULES)])
        dependents = online.downstream_dependencies(exclude_states=('uninstallable',))
        return set((online | dependents).mapped('name'))

    @api.model
    def _ov_remove_online_services(self):
        """Mark the online service modules and the modules depending on them
        for removal. Called at the end of a module loading, before the modules
        marked for removal are removed."""
        online = self.sudo().search([('name', 'in', ONLINE_SERVICE_MODULES), ('state', 'in', ('installed', 'to upgrade'))])
        if online:
            dependents = online.downstream_dependencies()
            _logger.info("Removing the online service modules: %s", ", ".join(sorted((online | dependents).mapped('name'))))
            # The accounts refer to the services with a restricted foreign key:
            # removing the modules would log a failed deletion of the services.
            # Their tables are dropped with the modules anyway.
            if 'iap.account' in self.env:
                self.env['iap.account'].sudo().with_context(active_test=False).search([('service_id', '!=', False)]).unlink()
            online.button_uninstall()

    # The industries are listed and downloaded from the publisher's app store
    # (base_import_module, T2.3). The list stays empty, nothing is downloaded.

    @api.model
    def _get_modules_from_apps(self, fields, module_type, module_name, domain=None, limit=None, offset=None):
        return []

    @api.model
    def _get_industry_categories_from_apps(self):
        return []

    def button_immediate_install_app(self):
        raise UserError(self.env._("This product does not use the publisher's app store."))
