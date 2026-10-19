import { _t } from "@web/core/l10n/translation";
import {
    ClientErrorDialog,
    ErrorDialog,
    NetworkErrorDialog,
    odooExceptionTitleMap,
    RedirectWarningDialog,
    RPCErrorDialog,
    WarningDialog,
} from "@web/core/errors/error_dialogs";
import { patch } from "@web/core/utils/patch";

// Odoo puts its name in front of every error title; ours stay neutral.
ErrorDialog.title = _t("Error");
ClientErrorDialog.title = _t("Client Error");
NetworkErrorDialog.title = _t("Network Error");

function rpcErrorTitles() {
    return {
        server: _t("Server Error"),
        script: _t("Client Error"),
        network: _t("Network Error"),
    };
}

patch(RPCErrorDialog.prototype, {
    inferTitle() {
        super.inferTitle();
        if (odooExceptionTitleMap.has(this.props.exceptionName)) {
            return;
        }
        const title = rpcErrorTitles()[this.props.type];
        if (title) {
            this.title = title;
        }
    },
});

patch(WarningDialog.prototype, {
    inferTitle() {
        const title = super.inferTitle();
        if (this.props.title || odooExceptionTitleMap.has(this.props.exceptionName)) {
            return title;
        }
        return _t("Warning");
    },
});

patch(RedirectWarningDialog.prototype, {
    setup() {
        super.setup();
        if (!this.props.subType) {
            this.title = _t("Warning");
        }
    },
});
