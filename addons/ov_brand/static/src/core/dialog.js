import { t } from "@odoo/owl";
import { dialogProps } from "@web/core/dialog/dialog";
import { patch } from "@web/core/utils/patch";
import { getBrandName } from "@ov_brand/brand";

// Dialogs opened without a title show the product name
patch(dialogProps, {
    title: t.string().optional(getBrandName()),
});
