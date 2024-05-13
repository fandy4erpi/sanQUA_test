from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging
from datetime import date


_logger = logging.getLogger(__name__)

class WizardPurchaseRequest(models.TransientModel):
    _name = 'wizard.purchase.request'

    @api.model
    def _get_default_request_by(self):
        user = self.env.uid
        return user

    @api.model
    def _get_now(self):
        return date.today()


    @api.model
    def _company_get(self):
        return self.env["res.company"].browse(self.env.company.id)

    purchase_request_id = fields.Many2one('purchase.request', string="Purcahse Request")
    partner_id = fields.Many2one('res.partner', string="Vendor")
    name = fields.Char(string="Name")
    request_by = fields.Many2one('res.users', string='Request By', required=True, default=_get_default_request_by)
    request_date = fields.Date(string='Date', required=True, default=_get_now)
    order_kategori = fields.Selection([
        ('baku', "Bahan Baku Produksi"),
        ('pendukung', "Bahan Pendukung Produksi"),
        ('asset', "Asset"),
        ('barang_khusus', 'Barang Khusus'),
        ('operational', 'Operational'),
        ('lain', 'Lain - Lain'),
    ], string='Order Kategori')

    company_id = fields.Many2one(
        comodel_name="res.company",
        tracking=True,
    )
    wizard_purchase_request_lines = fields.One2many('wizard.purchase.request.line', 'wizard_purchase_request_id', string='Purchase Request Lines')

    state = fields.Selection([
        ('draft','Draft'),
        ('close','Close')],
        string="Status",
    )

    def action_create_po(self):
        vals = {
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'currency_id': self.company_id.currency_id.id,
            'date_order': self.request_date,
        }
        purchase_order = self.env['purchase.order'].sudo().create(vals)
        for line in self.wizard_purchase_request_lines:
            vals = {
                'order_id':purchase_order.id,
                'product_id': line.product_id.id,
                'product_qty': line.quantity,
                'price_unit': line.price_total
            }
            purchase_order_line = self.env['purchase.order.line'].sudo().create(vals)


class WizardPurchaseRequestLine(models.TransientModel):
    _name = 'wizard.purchase.request.line'

    name = fields.Char(string="Description")
    product_id = fields.Many2one('product.product', string="Product")
    price_total = fields.Float(string="Price")
    quantity_plan = fields.Float(string="Qty", readonly="1")
    quantity = fields.Float(string="Qty Realeased")
    uom_id = fields.Many2one('uom.uom', string="Uom")
    wizard_purchase_request_id = fields.Many2one('wizard.purchase.request')