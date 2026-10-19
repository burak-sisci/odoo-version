import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";
import { getBrandName } from "@ov_brand/brand";

const { component: ResConfigEdition } = registry.category("view_widgets").get("res_config_edition");

patch(ResConfigEdition.prototype, {
    setup() {
        super.setup();
        this.ovBrandName = getBrandName();
    },
});
