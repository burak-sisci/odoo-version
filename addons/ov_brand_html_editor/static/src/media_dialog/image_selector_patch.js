import { ImageSelector } from "@html_editor/main/media/media_dialog/image_selector";
import { patch } from "@web/core/utils/patch";

// The illustrations come from the publisher's media library (T2.3)
patch(ImageSelector.prototype, {
    async fetchLibraryMedia() {
        return { media: [], results: null };
    },
});
