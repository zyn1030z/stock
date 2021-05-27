from datetime import datetime

import xlsxwriter

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SaleRequest(models.Model):
    _name = 'sale.request'
    _inherit = [
        'mail.thread'
    ]
    name = fields.Char('Mã yêu cầu', readonly=True, select=True, copy=True, default='New')
    warehouse_id = fields.Many2one('stock.warehouse', string='Mã kho/Cửa hàng')
    date_request = fields.Datetime('Ngày yêu cầu', default=datetime.today())
    state = fields.Selection([
        ('draft', 'Yêu cầu hàng bán'),
        ('sent', 'Yêu cầu hàng bán được gửi'),
        ('processed', 'Được xử lý')],
        string='Use status', default='draft', track_visibility='always')
    warehouse_process = fields.Boolean(default=False, string='Trạng thái xử lý của kho')
    purchase_process = fields.Boolean(default=False, string='Trạng thái xử lý của thu mua')
    sale_request_line = fields.One2many(comodel_name='sale.request.line', inverse_name='sale_request_id',
                                        string='Sale Request Lines')

    # @api.constrains('sale_request_line')
    # def _constraint_supply(self):
    def print_excel(self):
        workbook = xlsxwriter.Workbook('Expenses01.xlsx')
        worksheet = workbook.add_worksheet()
        print(workbook)
        print(worksheet)

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('sale.request.seq') or '/'
        d_to = datetime.today()
        name = 'SR.' + str(d_to.year) + str(d_to.strftime('%m'))
        vals['name'] = name + '.' + seq
        return super(SaleRequest, self).create(vals)

    def get_contract_template(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'pur_request/static/xls/imp_donmuahang.xls'
        }

    def open_import_stock(self):
        print('test')
        return {
            'name': 'Import file',
            'type': 'ir.actions.act_window',
            'res_model': 'import.xls.wizard.stock',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {'current_id': self.id},
        }

    def send_sale_request(self):
        # data_time_request = self.env['ir.config_parameter'].sudo().get_param('stock_custom.x_time_request')
        data_time_request = self.env['res.config.settings'].sudo().search([], order="id desc", limit=1)
        if not self.date_request < data_time_request.x_time_request:
            raise ValidationError(
                _('Quá thời gian chấp nhận yêu cầu'))
        self.state = 'sent'

    def return_sale_request(self):
        data_time_request = self.env['res.config.settings'].sudo().search([], order="id desc", limit=1)
        if not self.date_request < data_time_request.x_time_request:
            raise ValidationError(
                _('Quá thời gian chấp nhận yêu cầu'))
        self.state = 'draft'

    def accept_sale_request(self):
        # self.state = 'processed'
        product_lines = self.env['sale.request.line'].search([('sale_request_id', '=', self.id)])
        for pr_line in product_lines:
            print(pr_line.supply_type)
