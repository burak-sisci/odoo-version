import { Editor } from "@html_editor/editor";
import { TranslatePlugin } from "@html_editor/main/translate/translate_plugin";
import { MAIN_PLUGINS } from "@html_editor/plugin_sets";
import { patch } from "@web/core/utils/patch";

// "Translate with Google Translate" sends the selected text to the publisher's
// online service (T2.3). Removed from every editor, including the chatter.
patch(Editor.prototype, {
    preparePlugins() {
        const Plugins = this.config.Plugins || MAIN_PLUGINS;
        this.config = { ...this.config, Plugins: Plugins.filter((P) => P !== TranslatePlugin) };
        return super.preparePlugins(...arguments);
    },
});
