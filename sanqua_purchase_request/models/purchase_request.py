from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging
from datetime import date


_logger = logging.getLogger(__name__)

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _inherit = ["mail.thread", "mail.activity.mixin"]

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
        required=False,
        default=_company_get,
        tracking=True,
    )

    @api.model
    def _count_po(self):
        for rec in self:
            counts = 0
            counts = self.env['purchase.order'].sudo().search_count([('purchase_request_id','=',rec.id)])
            rec.summary_po_count = counts


    purchase_request_lines = fields.One2many('purchase.request.line', 'purchase_request_id', string='Purchase Request Lines')
    summary_po_count = fields.Integer(string="Purchase Order", compute='_count_po')

    is_read = fields.Boolean(default=False)
    state = fields.Selection([
        ('draft','Draft'),
        ('close','Close')],
        string="Status",
    )

    def button_close_po(self):
        self.write({'state':'close'})


    def button_create_po(self):

        wizard_purchase_request = self.env['wizard.purchase.request'].sudo().create({
            'purchase_request_id':self.id,
            'company_id':self.company_id.id
        })


        purchase_request_lines = []
        for line in self.purchase_request_lines:
            line = (0, 0, {
                'wizard_purchase_request_id': wizard_purchase_request.id,
                'product_id': line.product_id.id,
                'quantity_plan':line.quantity,
                'price_total':line.price_total
            })
            purchase_request_lines.append(line)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Request',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.purchase.request',
            'context': {'default_id':wizard_purchase_request,
                        'default_purchase_request_id': self.id,
                        'default_company_id':self.company_id.id,
                        'default_request_date':self.request_date,
                        'default_wizard_purchase_request_lines':purchase_request_lines},
            'target': 'new',
        }



    def open_po(self):
        po_list = self.env['purchase.order'].search([
            ('purchase_request_id','=',self.id),
        ])

        action = {
            'type': 'ir.actions.act_window',
            'name': _('Purchase Order'),
            'res_model': 'purchase.order',
            'view_type': 'list',
            'view_mode': 'list',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', 'in', [x.id for x in po_list])],
        }

        return action

    @api.model
    def create(self, vals):
        sequence = self.env["ir.sequence"].next_by_code("purchase.request")
        vals["name"] = sequence
        return super(PurchaseRequest, self).create(vals)



class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'

    purchase_request_id = fields.Many2one('purchase.request')
    name = fields.Char(string="Description")
    product_id = fields.Many2one('product.product', string="Product")
    price_total = fields.Float(string="Price")
    quantity = fields.Float(string="Quantity")
    uom_id = fields.Many2one('uom.uom', string="Uom")
    stock_on_hand = fields.Integer(string="Stock On Hand")