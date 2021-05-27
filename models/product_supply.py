from odoo import models, fields


class product(models.Model):
    _inherit = 'product.template'

    supply_type = fields.Selection([
        ('warehouse', 'Kho tổng'),
        ('purchase', 'Thu mua')],
        string='Thông tin danh mục hàng hóa', default='warehouse', track_visibility='always', required=True)
