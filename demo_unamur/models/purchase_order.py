
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    cpo = fields.Many2one('unamur.cpo', string='CPO')
