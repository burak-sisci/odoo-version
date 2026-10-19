import { session } from "@web/session";

/**
 * Product name users see, sent by the server in the session info
 * (`ov_brand.name` system parameter, see ov_brand/tools.py).
 *
 * @returns {string}
 */
export function getBrandName() {
    return session.ov_brand_name || "";
}
