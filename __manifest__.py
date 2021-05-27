# -*- coding: utf-8 -*-
{
    'name': 'Yêu cầu hàng bán ',
    'version': '1.0',
    'sequence': 1,
    'summary': 'Odoo 14 yêu cầu hàng bán',
    'description': """""",
    'category': 'Tutorials',
    'author': 'Hung Pham',
    'maintainer': '',
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'purchase',
        'stock',
        'report_xlsx'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/sale_request.xml',
        'views/import_xls_stock.xml',
        'report/sale_request_report.xml',
        'views/product_inherit_add_supply.xml',
        'views/resconfig_inherit.xml',
        'views/general_request_view.xml'
    ],
    'demo': [],
    'qweb': [],
    'images': [''],
    'installable': True,
    'auto_install': False,
    'application': True,
}
