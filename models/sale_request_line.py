from odoo import models, fields, api


class SaleRequestLine(models.Model):
    _name = 'sale.request.line'
    _inherit = [
        'mail.thread'
    ]
    sale_request_id = fields.Many2one(comodel_name='sale.request', string='Sale Request Reference',
                                      ondelete='cascade')
    # request_id = fields.Many2one('sale.request', string='Mã yêu cầu')
    request_id = fields.Char(related='sale_request_id.name', string='Mã yêu cầu')
    product_id = fields.Many2one('product.product', string='Sản phẩm', change_default=True)
    qty = fields.Float(string='Số lượng yêu cầu')
    qty_apply = fields.Float(string='Số lượng đáp ứng', default=0)
    product_uom = fields.Many2one('uom.uom', string='Đơn vị tính', related='product_id.uom_id')
    supply_type = fields.Selection('Đơn vị cung ứng', related='product_id.supply_type')

    # supply_type = fields.Many2one('product.product', 'Đơn vị cung ứng')
    # supply_type = fields.Selection([
    #     ('warehouse', 'Kho tổng'),
    #     ('purchase', 'Thu mua')],
    #     string='Thông tin danh mục hàng hóa', track_visibility='always')

    @api.constrains('product_id')
    def _onchange_product_supply(self):
        for rc in self:
            rc.supply_type = rc.product_id.supply_type
            print(rc.product_id.supply_type)

    @api.constrains('qty')
    def _constrain_qty(self):
        self.qty_apply = self.qty

    # @api.depends('product_id', 'supply_type')
    # def get_vendor_from_product(self):
    #     # print(self.sale_request_id.name)
    #     # self.request_id = self.sale_request_id.name
    #     for rc in self:
    #         default_code = rc.env['product.product'].search([('id', '=', rc.product_id.id)])
    #         product_tl_id = rc.env['product.template'].search([('default_code', '=', default_code.default_code)])
    #         for rec in product_tl_id:
    #             id_vendor = rc.env['product.supplierinfo'].search([('product_tmpl_id', '=', rec.id)], limit=1)
    #             name_vendor = id_vendor.name
    #             self.supply_type = id_vendor.name

    def get_contract_template(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'pur_request/static/xls/imp_phieuyeucauhanghoa.xlsx'
        }
