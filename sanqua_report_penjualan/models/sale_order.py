from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging
from datetime import date


_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    @api.model
    def print_xxx(self):
        so_list = []
        for data in self.env['sale.order.line'].sudo().search([]):
            do_number = False
            do_obj = self.env['stock.picking'].sudo().search([('origin','=',data.order_id.name)],limit=1)
            if do_obj:
                do_number = do_obj.name
            so_number = data.order_id.name
            customer_name = data.order_id.partner_id.display_name
            address = data.order_id.partner_id.contact_address
            delivery_date = False
            if do_obj:
                delivery_date = do_obj.date_done
            company = data.order_id.company_id.name
            product = data.product_id.name

            total_qty_return = 0
            grop_id_obj = self.env['procurement.group'].sudo().search([('name','=',data.order_id.name)],limit=1)
            if grop_id_obj:
                picking = self.env['stock.picking'].sudo().search([('location_dest_id','=',5),('group_id','=',grop_id_obj.id)])
                if picking:
                    move_line = self.env['stock.move.line'].sudo().search([('picking_id','=',picking.id),('product_id','=',data.product_id.id),('state','=','done')])
                    for line in move_line:
                        total_qty_return += line.qty_done

            demand = data.product_uom_qty
            qty_done = data.qty_delivered
            qty_return = total_qty_return
            qty_net = round(demand - qty_return,2)

            no_inv = ""
            inv_obj = self.env['account.move'].sudo().search([('invoice_origin','=',data.order_id.name)],limit=1)
            if inv_obj:
                no_inv = inv_obj.name
            total_inv = data.qty_invoiced
            so_list.append([do_number, so_number, customer_name,address, delivery_date, company, product, demand, qty_done, qty_return, qty_net, no_inv, total_inv])
        print(so_list)
        return so_list


