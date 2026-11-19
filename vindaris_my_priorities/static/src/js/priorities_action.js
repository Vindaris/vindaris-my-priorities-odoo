/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

// The "My Priorities" screen. On open it asks the Odoo backend for this user's
// Vindaris embed URL and iframes it. If the account is not linked yet it shows
// a Connect button; if the admin has not connected Odoo to Vindaris it says so.
export class VindarisPriorities extends Component {
    static template = "vindaris_my_priorities.VindarisPriorities";
    static props = ["*"];

    setup() {
        this.state = useState({ status: "loading", embedUrl: null, linkUrl: null });
        onWillStart(async () => {
            try {
                const res = await rpc("/vindaris/priorities/url");
                if (res && res.embedUrl) {
                    this.state.embedUrl = res.embedUrl;
                    this.state.status = "ready";
                } else if (res && res.linkUrl) {
                    this.state.linkUrl = res.linkUrl;
                    this.state.status = "connect";
                } else if (res && res.status === "unconfigured") {
                    this.state.status = "unconfigured";
                } else {
                    this.state.status = "error";
                }
            } catch {
                this.state.status = "error";
            }
        });
    }
}

registry.category("actions").add("vindaris_my_priorities.priorities", VindarisPriorities);
