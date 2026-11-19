import requests

from odoo import http
from odoo.http import request

# Server-to-server bridge the OWL client action calls. It reads the module's
# own credentials (never exposed to the browser), asks Vindaris for the current
# user's embed URL, and returns it. The Odoo user id is taken from the
# authenticated session, so a user can only ever request their own priorities.

SESSION_PATH = "/api/embed/odoo/session"
DEFAULT_BASE_URL = "https://app.vindaris.com"


class VindarisPriorities(http.Controller):
    @http.route("/vindaris/priorities/url", type="json", auth="user")
    def priorities_url(self):
        icp = request.env["ir.config_parameter"].sudo()
        base_url = (icp.get_param("vindaris.base_url") or DEFAULT_BASE_URL).strip().rstrip("/")
        instance_id = icp.get_param("vindaris.instance_id")
        secret = icp.get_param("vindaris.instance_secret")
        if not instance_id or not secret:
            return {"status": "unconfigured"}

        try:
            resp = requests.post(
                base_url + SESSION_PATH,
                headers={
                    "x-odoo-instance-id": instance_id,
                    "x-odoo-instance-secret": secret,
                    "content-type": "application/json",
                },
                json={"odooUid": request.env.uid},
                timeout=20,
            )
            resp.raise_for_status()
            return resp.json()
        except Exception:  # noqa: BLE001 - the client shows a generic retry message
            return {"status": "error"}
