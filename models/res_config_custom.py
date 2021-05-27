from datetime import datetime

from odoo import models, fields, api


class ResConfigCustom(models.TransientModel):
    _inherit = 'res.config.settings'

    x_time_request = fields.Datetime(string='Thời gian chốt nhận yêu cầu', default=datetime.today())
    x_sequence = fields.Integer(string='Số thứ tự')

    @api.model
    def get_values(self):
        res = super(ResConfigCustom, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res.update(
            x_time_request=ICPSudo.get_param('x_time_request'),
        )

        return res
