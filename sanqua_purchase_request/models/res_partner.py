from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging
from datetime import date


_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _check_partner(self):
        for rec in self:
            if rec.customer_rank > 0:
                rec.is_customer = True
            else:
                rec.is_customer = False

            if rec.supplier_rank > 0:
                rec.is_supplier = True
            else:
                rec.is_supplier = False


    is_customer = fields.Boolean(compute='_check_partner')
    is_supplier = fields.Boolean(compute='_check_partner')