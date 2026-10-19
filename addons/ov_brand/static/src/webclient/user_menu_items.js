import { registry } from "@web/core/registry";
import { session } from "@web/session";

// Without ov_brand.support_url, the "Help" item would open an empty page
if (!session.support_url) {
    registry.category("user_menuitems").remove("support");
}
