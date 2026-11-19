import requests

from odoo import api, fields, models
from odoo.exceptions import UserError

# Connection settings for the Vindaris "My Priorities" module. The admin enters
# the Vindaris URL and clicks Connect once; the module registers with Vindaris
# and stores its own instanceId + secret as system parameters. The secret is
# never shown in the UI, only its presence (Connected / Disconnect).

REGISTER_PATH = "/api/embed/odoo/register"
DEFAULT_BASE_URL = "https://app.vindaris.com"

PARAM_BASE_URL = "vindaris.base_url"
PARAM_INSTANCE_ID = "vindaris.instance_id"
PARAM_INSTANCE_SECRET = "vindaris.instance_secret"


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    vindaris_base_url = fields.Char(
        string="Vindaris URL",
        config_parameter=PARAM_BASE_URL,
        default=DEFAULT_BASE_URL,
    )
    # The instanceId is safe to surface; the secret is deliberately NOT a field.
    vindaris_instance_id = fields.Char(
        string="Connection ID",
        config_parameter=PARAM_INSTANCE_ID,
        readonly=True,
    )
    vindaris_connected = fields.Boolean(compute="_compute_vindaris_connected")

    @api.depends("vindaris_instance_id")
    def _compute_vindaris_connected(self):
        for rec in self:
            rec.vindaris_connected = bool(rec.vindaris_instance_id)

    def _vindaris_base_url(self):
        return (self.vindaris_base_url or DEFAULT_BASE_URL).strip().rstrip("/")

    def action_vindaris_connect(self):
        self.ensure_one()
        base_url = self._vindaris_base_url()
        if not base_url:
            raise UserError("Enter the Vindaris URL first.")

        icp = self.env["ir.config_parameter"].sudo()
        own_url = icp.get_param("web.base.url")
        try:
            resp = requests.post(
                base_url + REGISTER_PATH,
                json={"baseUrl": own_url},
                timeout=20,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:  # noqa: BLE001 - surface any failure to the admin
            raise UserError("Could not reach Vindaris to connect: %s" % exc)

        instance_id = data.get("instanceId")
        secret = data.get("secret")
        if not instance_id or not secret:
            raise UserError("Vindaris did not return connection credentials.")

        icp.set_param(PARAM_BASE_URL, base_url)
        icp.set_param(PARAM_INSTANCE_ID, instance_id)
        icp.set_param(PARAM_INSTANCE_SECRET, secret)
        return {"type": "ir.actions.client", "tag": "reload"}

    def action_vindaris_disconnect(self):
        icp = self.env["ir.config_parameter"].sudo()
        icp.set_param(PARAM_INSTANCE_ID, "")
        icp.set_param(PARAM_INSTANCE_SECRET, "")
        return {"type": "ir.actions.client", "tag": "reload"}
