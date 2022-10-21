from odoo import models, fields, api


class CrossoveredBudget(models.Model):
    _inherit = "crossovered.budget"

    budget_type = fields.Selection([
        ('ordinaire', 'Ordinaire'), ('extraordinaire', 'Extraordinaire')],
        string="Type", default="ordinaire",
    )


class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    cpo = fields.Many2one('unamur.cpo', string='CPO')
    amount_total = fields.Monetary(string='Engagé', compute="_compute_amount")
    requisition_amount_total = fields.Monetary(string="Contrat d'engagement")

    @api.depends("cpo")
    def _compute_amount(self):
        for budget in self:
            budget.amount_total = sum(self.env["purchase.order"].search([("cpo", "=", budget.cpo.id)]).mapped(
                "amount_total")) if budget.cpo else 0.0
            budget.requisition_amount_total = sum(
                (self.env["purchase.requisition"].search([("cpo", "=", budget.cpo.id)]).mapped(
                    "line_ids")).mapped("price_unit")) if budget.cpo else 0.0


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    cpo = fields.Many2one("unamur.cpo", string="CPO")


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    cpo = fields.Many2one('unamur.cpo', string="CPO", compute="_compute_cpo")
    attachment_number = fields.Integer('Documents', compute='_compute_attachment_number')

    @api.depends("line_ids")
    def _compute_cpo(self):
        """
        Return the first Analytic Account found in order_line
        """
        for purchase in self:
            cpo = purchase.line_ids.mapped("cpo")
            purchase.cpo = cpo if len(cpo) == 1 else False

    def _compute_attachment_number(self):
        attachment_data = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'purchase.requisition'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for requisition in self:
            requisition.attachment_number = attachment.get(requisition._origin.id, 0)

    def action_get_attachment_view(self):
        self.ensure_one()
        res = self.env['ir.actions.act_window']._for_xml_id('base.action_attachment')
        res['domain'] = [('res_model', '=', 'purchase.requisition'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'purchase.requisition', 'default_res_id': self.id}
        return res
