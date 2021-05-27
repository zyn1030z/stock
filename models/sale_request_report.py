from odoo import models


class SaleRequestReport(models.AbstractModel):
    _name = 'report.sale.request.report'
    # _inherit = 'report.report_xlsx.abstract'
    _inherit = 'report.report_xlsx.partner_xlsx'

    def generate_xlsx_report(self, workbook, data, lines):
        # format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        # sheet = workbook.add_worksheet('Request Sale Report')
        # sheet.write(2, 2, 'name', format1)
        # sheet.write(2, 3, lines.name, format1)
        for obj in lines:
            # One sheet by partner
            format1 = workbook.add_format({'font_size': 12, 'align': 'center', 'bold': True})
            format2 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': False})
            format5 = workbook.add_format({'font_size': 10, 'align': 'right', 'bold': False})
            format4 = workbook.add_format({'font_size': 10, 'bold': False})
            format3 = workbook.add_format({'font_size': 18, 'align': 'center', 'bold': True})
            sheet = workbook.add_worksheet(obj.name)
            sheet.set_column(0, 5, 24)
            sheet.set_column(6, 6, 30)
            sheet.set_row(4, 30)
            sheet.set_row(10, 25)
            sheet.write(2, 2, 'name', format1)
            sheet.insert_image('A1',
                               '/home/zyn1030z/Documents/dev/odoo-14.0/odoo14-custom-addons/stock_custom/static/src/img/image.png')
            sheet.merge_range('C1:G1', 'CÔNG TY CỔ PHẦN QUỐC TẾ HOMEFARM', format1)
            sheet.merge_range('C2:G2', 'Địa chỉ: 14 Nguyễn Cảnh Dị, Hoàng Mai, Hà Nội', format2)
            sheet.merge_range('C3:G3', 'Hotline:    02471081008    ', format2)
            sheet.merge_range('C4:G4', 'Email:  dathang@homefarm.vn      Website: https://homefarm.vn/', format2)
            sheet.merge_range('A5:G5', 'PHIẾU YÊU CẦU CUNG ỨNG HÀNG HÓA', format3)
            sheet.write('E6', 'Số phiếu yêu cầu: ', format4)
            sheet.write('E7', 'Ngày yêu cầu: ', format4)
            sheet.write('E8', 'Trạng thái phiếu: ', format4)
            sheet.write('A9', 'Cửa hàng/ Kho yêu cầu:', format4)
            sheet.write('B9', obj.warehouse_id.name, format2)
            sheet.write('B10', obj.warehouse_id.partner_id.name, format2)
            sheet.write('A10', 'Địa chỉ', format2)
            sheet.write('A11', 'STT', format2)
            sheet.write('B11', 'Mã hàng hóa', format2)
            sheet.write('C11', 'Tên hàng hóa', format2)
            sheet.write('D11', 'Đơn vị đặt hàng', format2)
            sheet.write('E11', 'Số lượng yêu cầu', format2)
            sheet.write('F11', 'Số lượng đáp ứng', format2)
            sheet.write('G11', 'Đơn vị cung ứng'
                               '(warehouse/purchase)', format2)
            sheet.write(2, 3, obj.name, format1)
            sheet.write(2, 3, obj.date_request, format1)
            sheet.write(2, 3, obj.state, format1)
            sale_request_lines = obj.sale_request_line
            sheet.write('F6', obj.name, format2)
            sheet.write('F7', obj.date_request, format2)
            sheet.write('F8', obj.state, format2)
            row_num = 12
            stt = 1
            sum_qty = 0
            sum_qty_supply = 0
            for sale_request_line in sale_request_lines:
                sheet.write('C' + str(row_num), sale_request_line.product_id.name, format2)
                sheet.write('A' + str(row_num), stt, format2)
                sheet.write('B' + str(row_num), sale_request_line.product_id.default_code, format2)
                sheet.write('E' + str(row_num), sale_request_line.qty, format2)
                sheet.write('F' + str(row_num), sale_request_line.qty_apply, format2)
                sheet.write('G' + str(row_num), sale_request_line.supply_type, format2)
                row_num += 1
                stt += 1
                sum_qty += sale_request_line.qty
                sum_qty_supply += sale_request_line.qty_apply

            sheet.merge_range('A' + str(row_num) + ':' + 'D' + str(row_num), 'Tổng cộng', format5)
            sheet.write('E' + str(row_num), sum_qty, format2)
            sheet.write('F' + str(row_num), sum_qty_supply, format2)
            sheet.merge_range('C' + str(row_num + 2) + ':' + 'D' + str(row_num + 2), 'Quản lý Cửa hàng/ Kho tổng',
                              format2)
            sheet.merge_range('C' + str(row_num + 3) + ':' + 'D' + str(row_num + 3), '(Ký,ghi rõ họ tên)', format2)
            sheet.merge_range('F' + str(row_num + 2) + ':' + 'G' + str(row_num + 2), 'Lập phiếu', format2)
            sheet.merge_range('F' + str(row_num + 3) + ':' + 'G' + str(row_num + 3), '(Ký,ghi rõ họ tên)', format2)
            border_format = workbook.add_format({
                'border': 1,
                'align': 'left',
                'font_size': 10
            })
            sheet.conditional_format(10, 0, row_num, 6, {'type': 'no_blanks', 'format': border_format})
            sheet.conditional_format(8, 0, 9, 1, {'type': 'no_blanks', 'format': border_format})
