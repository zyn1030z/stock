import base64
import binascii
import tempfile

import xlrd

from odoo import models, fields, _
from odoo.exceptions import ValidationError


class ImportFileStock(models.TransientModel):
    _name = 'import.xls.wizard.stock'
    # xls_file_stock = fields.Binary(string='File Excel', required=True)
    upload_file = fields.Binary(string="Upload File")
    file_name = fields.Char(string="File Name")

    def check_exist_product_in_database(self, values):
        arr_line_error_not_exist_database = []
        line_check_exist_data = 7
        for val in values[6:]:
            product_id_import = self.env['product.product'].search(
                [('default_code', '=', val[0])]).id  # product_id trong file import
            if product_id_import is False:
                arr_line_error_not_exist_database.append(line_check_exist_data)
            line_check_exist_data += 1
        return arr_line_error_not_exist_database

    def _check_product_qty_in_excel(self, values):
        arr_line_error_slsp = []
        line_check_slsp = 7
        for val in values[6:]:
            if not val[2]:
                arr_line_error_slsp.append(line_check_slsp)
            elif float(val[2]) < 0:
                arr_line_error_slsp.append(line_check_slsp)
            line_check_slsp += 1
        return arr_line_error_slsp

    def create_product(self, val, amount, product_uom, ):
        product_id_import = self.env['product.product'].search(
            [('default_code', '=', val[0])]).id
        self.env['sale.request.line'].create(
            {'qty': float(val[2]), 'sale_request_id': amount,
             'product_id': product_id_import, 'product_uom': product_uom})
        self.env.cr.commit()

    def import_xls_stock(self):
        amount = self.env.context.get('current_id')
        print('amount', amount)
        try:
            wb = xlrd.open_workbook(file_contents=base64.decodestring(self.upload_file))
        except:
            raise ValidationError(
                'File import phải là file excel')
        values = []
        for sheet in wb.sheets():
            for row in range(sheet.nrows):
                col_values = []
                for col in range(sheet.ncols):
                    value = sheet.cell(row, col).value
                    try:
                        value = str(value)
                    except:
                        pass
                    col_values.append(value)
                values.append(col_values)
        arr_line_error_slsp = self._check_product_qty_in_excel(values)
        arr_line_error_not_exist_database = self.check_exist_product_in_database(values)
        listToStr_line_slsp = ' , '.join([str(elem) for elem in arr_line_error_slsp])
        listToStr_line_not_exist_database = ' , '.join([str(elem) for elem in arr_line_error_not_exist_database])
        print(len(arr_line_error_not_exist_database))
        if len(arr_line_error_not_exist_database) == 0 and len(arr_line_error_slsp) == 0:
            exist_products_in_line = self.env['sale.request.line'].search([('sale_request_id', '=', amount)])
            exist_products_in_line_arr = []
            for pr_in_line in exist_products_in_line:
                exist_products_in_line_arr.append(pr_in_line.product_id.default_code)
            # tạo mảng lưu mã sản phẩm trong bảng chi tiết không lặp lại ex : [code1, code2]
            arr = []
            for r in exist_products_in_line_arr:
                if r not in arr:
                    arr.append(r)
            print('arr', arr)
            for val in values[6:]:
                if len(arr) != 0:
                    if val[0] in arr:
                        print('hh')
                        id_product_exist = self.env['product.product'].search(
                            [('default_code', '=', val[0])]).id
                        rc_purchase_order_line_exist_list = self.env['sale.request.line'].search(
                            [('product_id', '=', id_product_exist), ('sale_request_id', '=', amount)])
                        print(rc_purchase_order_line_exist_list)
                        for rc_purchase_order_line_exist in rc_purchase_order_line_exist_list:
                            product_quanty = rc_purchase_order_line_exist.qty + float(
                                val[2])
                            rc_purchase_order_line_exist.write({'qty': product_quanty})
                    else:
                        break
                else:
                    product_id_import_standard = self.env['product.product'].search(
                        [('default_code', '=', val[0])]).product_tmpl_id.id
                    uom = self.env['product.template'].search(
                        [('id', '=', product_id_import_standard)]
                    ).uom_id
                    uom_current = self.env['uom.uom'].search([('name', '=', uom.name)]).id
                    self.create_product(val, amount, uom_current)
        elif len(arr_line_error_not_exist_database) != 0:
            raise ValidationError(
                _('Sản phẩm không tồn tại trong hệ thống, dòng (%s)') % str(listToStr_line_not_exist_database))
        elif len(arr_line_error_slsp) != 0:
            raise ValidationError(
                _('Số lượng sản phẩm phải lớn hơn 0 hoặc không để trống, dòng (%s)') % str(listToStr_line_slsp))
