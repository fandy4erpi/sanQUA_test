{
    'name': 'Report Penjualan Bersih',
    'version': '15.0.0.0',
    'category': 'Uncategorized',
    'license': 'OPL-1',
    'summary': 'Report Penjualan Bersih',
    'description': """ - """,
    'author': 'Arief Afandy',
    'depends': ['base','sale','sanqua_purchase_request'],
    'data': [
            'security/ir.model.access.csv',
            'report/report_penjualan_bersih.xml',
            'report/template_penjualan_bersih.xml',
            'wizard/wizard_report_penjualan.xml'
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
