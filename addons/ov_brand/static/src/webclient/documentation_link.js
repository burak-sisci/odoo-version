import { patch } from "@web/core/utils/patch";
import { DocumentationLink } from "@web/views/widgets/documentation_link/documentation_link";

// The publisher's documentation (T2.3). The product has no documentation site
// of its own yet (T8.7).
const PUBLISHER_DOCUMENTATION = /^https?:\/\/(www\.)?odoo\.com\//;

patch(DocumentationLink.prototype, {
    get ovHidden() {
        return PUBLISHER_DOCUMENTATION.test(this.url);
    },
});
