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
    purchase_order_id = fields.Many2one('purchase.order', string='PO')
    amount_total = fields.Monetary(string='Engagé', related="purchase_order_id.amount_total")
    purchase_requisition_id = fields.Many2one('purchase.requisition', string="Contrat d'engagement",
                                              related="purchase_order_id.requisition_id")
    requisition_amount_total = fields.Monetary(string="Contrat d'engagement",
                                               compute="_compute_requisition_amount_total")

    @api.depends("purchase_requisition_id", "purchase_order_id")
    def _compute_requisition_amount_total(self):
        for budget in self:
            budget.requisition_amount_total = sum(budget.purchase_requisition_id.line_ids.mapped("price_unit"))


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    cpo = fields.Many2one("unamur.cpo", string="CPO")


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    cpo = fields.Many2one('unamur.cpo', string="CPO")
    attachment_number = fields.Integer('Documents', compute='_compute_attachment_number')

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
