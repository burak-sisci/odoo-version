from odoo import api, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type == 'form':
            self._ov_remove_online_service_settings(arch)
        return arch, view

    @api.model
    def _ov_remove_online_service_settings(self, arch):
        """Remove the settings that would install a module needing the
        publisher's online services (``module_<name>`` check boxes)."""
        online = None
        for node in arch.xpath("//field[starts-with(@name, 'module_')]"):
            if online is None:
                online = self.env['ir.module.module']._ov_online_service_dependents()
            if node.get('name').removeprefix('module_') not in online:
                continue
            box = next((
                ancestor for ancestor in node.iterancestors()
                if ancestor.tag == 'setting' or 'o_setting_box' in (ancestor.get('class') or '').split()
            ), node)
            parent = box.getparent()
            if parent is None:  # already removed with another check box
                continue
            parent.remove(box)
            # A block left without settings would only show its title
            while parent.tag == 'block' and not any(isinstance(child.tag, str) for child in parent):
                block, parent = parent, parent.getparent()
                parent.remove(block)
