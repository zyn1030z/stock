from odoo import fields, models


class WarehouseSupply(models.Model):
    _name = 'warehouse.supply'
    warehoue_source_id = fields.Many2one('stock.warehouse', string='Kho nguồn')
    warehoue_des_id = fields.Many2one('stock.warehouse', string='Kho đích')
