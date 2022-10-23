from odoo.addons.website.controllers.form import WebsiteForm
from odoo.http import request, route
from odoo import http, fields, _


class PortalExpense(WebsiteForm):
    def insert_record(self, request, model, values, custom, meta=None):
        res = []
        is_expense_model = model.model == "hr.expense"
        custom_values = custom.split("\n")
        if is_expense_model and custom:
            custom = ""
        for val in custom_values:
            res.append(map(str.strip, val.split(":", 1)))
        res = dict(res)
        res["employee_id"] = request.env.user.employee_id.id
        res["date"] = fields.Datetime.today()
        res["product_id"] = int(res["product_id"])
        product = request.env["product.product"].sudo().browse(res["product_id"])
        if product:
            res["unit_amount"] = product.price_compute('standard_price')[product.id]
            res["product_uom_id"] = int(product.uom_id.id)
        return super(PortalExpense, self).insert_record(request, model, res, custom, meta=meta)

    @route(["/expense"], type="http", auth="public", website=True)
    def u_namur_expense_form(self, **post):
        values = {}
        products = request.env["product.product"].sudo().search([("can_be_expensed", "=", True)])
        cpos = request.env["unamur.cpo"].sudo().search([])
        values.update(
            {
                "page_name": "my_expense_form",
                "products": products,
                "cpos": cpos,
                "employee": request.env.user.employee_id,
            }
        )
        response = request.render("demo_unamur.expense", values)

        return response
