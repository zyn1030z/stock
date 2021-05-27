from odoo import fields, models
from datetime import datetime


class GeneralRequest(models.Model):
    _name = 'general.request'
    _description = 'Tổng hợp yêu cầu'
    _inherit = [
        'mail.thread'
    ]
    warehouse_id = fields.Many2one('stock.warehouse', string='Kho')
    date = fields.Datetime(string='Ngày tổng hợp', default=datetime.today())
    state = fields.Selection([
        ('draft', 'Bản nháp'),
        ('received', 'Đã gửi'),
        ('done', 'Xử lý'),
        ('cancel', 'Hủy bỏ'), ],
        string='Use status', default='draft', track_visibility='always')
    general_request_line = fields.One2many(comodel_name='general.request.line', inverse_name='general_request_id',
                                           string='General Request Lines')


class GeneralRequestLine(models.Model):
    _name = 'general.request.line'
    _description = 'Tổng hợp yêu cầu chi tiết'
    general_request_id = fields.Many2one(comodel_name='general.request', string='General Request Reference',
                                         ondelete='cascade')
    # request_line_id = fields.Char(related='sale_request_id.name', string='Mã yêu cầu')
    # request_line_id map với sale_request_line_id
    request_line_id = fields.Char(string='ID yêu cầu')
    product_id = fields.Many2one('product.product', string='Sản phẩm', change_default=True)
    product_uom = fields.Many2one('uom.uom', string='Đơn vị tính', related='product_id.uom_id')
    warehoue_des_id = fields.Many2one('warehouse.supply', string='Kho nhận hàng')
    qty = fields.Float(string='Số lượng yêu cầu')
    qty_apply = fields.Float(string='Số lượng đáp ứng', default=0)
    stock_transfer_id = fields.Char(string='Phiếu chuyển kho nội bộ')
