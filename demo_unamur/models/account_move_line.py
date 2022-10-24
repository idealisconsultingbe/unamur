from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    journal_code = fields.Char(related="journal_id.code")


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    cpo = fields.Many2one('unamur.cpo', copy=False, string='CPO')

    @api.model_create_multi
    def create(self, vals_list):
        return super(AccountMoveLine, self).create(vals_list)
