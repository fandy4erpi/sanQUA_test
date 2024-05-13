from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging
from datetime import date


_logger = logging.getLogger(__name__)

class WizardReportPenjualan(models.TransientModel):
    _name = 'wizard.report.penjualan'

    name = fields.Char(string="Name")


    def action_print_report(self):
        sale_self = self.env['sale.order'].sudo().search([],limit=1)
        return self.env.ref('sanqua_report_penjualan.penjualan_bersih_action').report_action(sale_self)



