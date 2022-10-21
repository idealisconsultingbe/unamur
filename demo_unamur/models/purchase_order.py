
from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    cpo = fields.Many2one('unamur.cpo', string='CPO')
