from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    cpo = fields.Many2one('unamur.cpo', string='CPO')
