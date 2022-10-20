from odoo import api, fields, models


class UnamurCpo(models.Model):
    _name = "unamur.cpo"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Code", copy=False, compute="_compute_name")
    cpo_first_number = fields.Char(string="First Number", default="0000000", required=True)
    cpo_second_number = fields.Char(string="Second Number", default="000")
    is_readonly = fields.Boolean(string="is_readonly")
    partner_id = fields.Many2one('res.partner', string='Client')
    group_id = fields.Many2one('account.analytic.group', 'Groupe')
    description = fields.Text(string='Description')

    @api.model
    def _get_computed_name(self, cpo_first_number, cpo_second_number):
        return " ".join(p for p in (cpo_first_number, cpo_second_number) if p)

    @api.depends("cpo_first_number", "cpo_second_number")
    def _compute_name(self):
        for record in self:
            record.name = record._get_computed_name(record.cpo_first_number, record.cpo_second_number)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "cpo_first_number" in vals:
                vals["is_readonly"] = True
        return super(UnamurCpo, self).create(vals_list)
