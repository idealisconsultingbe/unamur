from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    cpo = fields.Many2one('unamur.cpo', string='CPO')


class Users(models.Model):
    _inherit = "res.users"

    cpo_ids = fields.Many2many('unamur.cpo', string='CPO')
