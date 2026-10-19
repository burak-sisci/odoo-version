import { browser } from "@web/core/browser/browser";
import { router, routerBus, startRouter } from "@web/core/browser/router";
import { patch } from "@web/core/utils/patch";
import { Many2One } from "@web/views/fields/many2one/many2one";
import { NavBar } from "@web/webclient/navbar/navbar";
import { WebClient } from "@web/webclient/webclient";

// The web client is served at /app instead of /odoo (T2.4, tools.py). The
// router keeps working with the upstream path; only the URLs users see change.
// Links still built with /odoo work through a redirection of the server.
export const WEB_PATH = "/app";
const UPSTREAM_PATH = /^\/odoo(?=[/?#]|$)/;
const OWN_PATH = /^\/app(?=[/?#]|$)/;

/**
 * Return the URL, a path, with the web client path in place of the upstream one.
 *
 * @param {string} url
 * @returns {string}
 */
export function webPath(url) {
    return url.replace(UPSTREAM_PATH, WEB_PATH);
}

patch(router, {
    stateToUrl(state) {
        return webPath(super.stateToUrl(state));
    },
    urlToState(urlObj) {
        if (OWN_PATH.test(urlObj.pathname)) {
            urlObj = new URL(urlObj);
            urlObj.pathname = urlObj.pathname.replace(OWN_PATH, "/odoo");
        }
        return super.urlToState(urlObj);
    },
});

// The router read the URL when it was loaded, before this patch
startRouter();
if (UPSTREAM_PATH.test(browser.location.pathname)) {
    // An old /web#... URL, just rewritten with the upstream path
    const { pathname, search, hash } = browser.location;
    browser.history.replaceState(browser.history.state, "", webPath(pathname) + search + hash);
}

// The router follows internal links in place only when the page is at the
// upstream path. Same handling at the web client path.
browser.addEventListener("click", (ev) => {
    if (
        ev.defaultPrevented ||
        ev.target.closest("[contenteditable]") ||
        !OWN_PATH.test(browser.location.pathname)
    ) {
        return;
    }
    const a = ev.target.closest("a");
    const href = a?.getAttribute("href");
    if (!href || href.startsWith("#") || a.target === "_blank") {
        return;
    }
    let url;
    try {
        url = new URL(a.href);
    } catch {
        return;
    }
    if (
        url.host === browser.location.host &&
        (url.pathname === "/web" || UPSTREAM_PATH.test(url.pathname) || OWN_PATH.test(url.pathname))
    ) {
        ev.preventDefault();
        router.pushState(router.urlToState(url), { replace: true, sync: true });
        browser.setTimeout(() => routerBus.trigger("ROUTE_CHANGE"));
    }
});

patch(WebClient.prototype, {
    registerServiceWorker() {
        // Same registration, with the scope of the web client path; the server
        // allows it (Service-Worker-Allowed)
        const container = navigator.serviceWorker;
        if (!container) {
            return super.registerServiceWorker();
        }
        const register = container.register;
        container.register = (scriptURL, options) =>
            register.call(container, scriptURL, { ...options, scope: WEB_PATH });
        try {
            return super.registerServiceWorker();
        } finally {
            delete container.register;
        }
    },
});

// Links shown on hover and opened in a new tab
patch(NavBar.prototype, {
    getMenuItemHref(payload) {
        return webPath(super.getMenuItemHref(payload));
    },
});

patch(Many2One.prototype, {
    get linkHref() {
        return webPath(super.linkHref);
    },
});
