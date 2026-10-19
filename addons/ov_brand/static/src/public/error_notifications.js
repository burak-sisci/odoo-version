import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

const errorNotifications = registry.category("error_notifications");

// Same notification as Odoo's, without its name in the texts
for (const exceptionName of [
    "odoo.http.session.SessionExpiredException",
    "werkzeug.exceptions.Forbidden",
]) {
    errorNotifications.add(
        exceptionName,
        {
            ...errorNotifications.get(exceptionName),
            title: _t("Session Expired"),
            message: _t("Your session expired. The current page is about to be refreshed."),
        },
        { force: true }
    );
}
