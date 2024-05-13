# -*- coding: utf-8 -*-
{
    'name': "Purchase_Request",
    'summary': """
        Modul pengajuan pembelian barang sebelum terbit sebuah PO""",
    'description': """
        Modul pengajuan pembelian barang sebelum terbit sebuah PO
    """,
    'author': "Arief Afandy",
    'website': "",
    'category': 'Uncategorized',
    'version': '15.0.0.1',
    'depends': [
        'web',
        'base',
        'purchase',
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/purchase_request_view.xml',
        'views/res_partner.xml',
        'wizard/purchase_request_wizard.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'OEEL-1',
}
