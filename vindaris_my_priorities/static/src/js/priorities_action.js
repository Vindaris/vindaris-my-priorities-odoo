/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

// "My Priorities" screen. It mounts an iframe of the hosted Vindaris embed page,
// which handles sign-in and renders the user's goals and tasks. All logic lives
// in Vindaris, so this module carries no server code and imports on Odoo Online.
//
// Note: the template binds the iframe src as "this.src" (not bare "src"). On the
// Odoo 19 OWL build, a bare identifier in a template expression does not resolve
// to the component instance field, so the attribute would stay empty.
const VINDARIS_EMBED_URL = "https://app.vindaris.com/embed/odoo";

export class VindarisPriorities extends Component {
    static template = "vindaris_my_priorities.VindarisPriorities";
    static props = ["*"];

    setup() {
        this.src = VINDARIS_EMBED_URL;
    }
}

registry.category("actions").add("vindaris_my_priorities.priorities", VindarisPriorities);
