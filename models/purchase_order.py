# -*- coding: utf-8 -*-
#################################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2017-2026 Hadron for Business sp. z o.o. (http://hadronforbusiness.com)
#
# This program is proprietary software, licensed under the Odoo Proprietary
# License v1.0 (OPL-1). Its use is governed by the Odoo Apps terms available
# at https://www.odoo.com/documentation/user/legal/licenses.html and the
# license agreement accepted at purchase / installation.
#
# It is forbidden to publish, distribute, sublicense, or sell copies of the
# Software or modified copies of the Software.
#
# The above copyright notice and this permission notice must be included in
# all copies or substantial portions of the Software.
#
#################################################################################
"""	@version	18.0.1.0.0
	@owner  Hadron for Business
	@author Hadron for Business sp. z o.o.
	@date   2026.10.07

	Product Cost from Purchase Orders - update on confirmation
	When a purchase order is approved, writes the net unit price of each line
	into the cost of products using the Standard Price costing method (converted
	to the product unit and company currency, several lines of one product
	averaged by quantity) and logs the change in the product chatter.
"""
from collections import defaultdict

from markupsafe import Markup

from odoo import _, fields, models
from odoo.tools import float_compare, float_is_zero


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_approve(self, force=False):
        # button_approve is the step that really turns an RFQ into a purchase
        # order: it is called by button_confirm when no approval is needed and
        # by the manager when the order waits in "To Approve".
        before = {order.id: order.state for order in self}
        result = super().button_approve(force=force)
        approved = self.filtered(
            lambda o: before.get(o.id) != o.state and o.state in ('purchase', 'done'))
        approved._update_product_cost()
        return result

    def _cost_is_updatable(self, product):
        """Hook: return False to keep the cost of a product untouched."""
        cost_method = getattr(product, 'cost_method', 'standard')
        return cost_method == 'standard'

    def _update_product_cost(self):
        for order in self.filtered(lambda o: o.company_id.po_update_product_cost):
            company = order.company_id
            date = order.date_order or fields.Datetime.now()
            totals = defaultdict(lambda: [0.0, 0.0, 0.0])  # cost in company currency, qty, price
            for line in order.order_line:
                product = line.product_id
                if line.display_type or not product or float_is_zero(
                        line.product_qty, precision_rounding=line.product_uom.rounding):
                    continue
                product = product.with_company(company)
                if not order._cost_is_updatable(product):
                    continue
                qty = line.product_uom._compute_quantity(line.product_qty, product.uom_id)
                if float_is_zero(qty, precision_rounding=product.uom_id.rounding):
                    continue
                subtotal = line.price_subtotal
                if float_is_zero(subtotal, precision_rounding=order.currency_id.rounding):
                    continue  # free goods / samples must not wipe the cost
                total = totals[product]
                total[0] += order.currency_id._convert(subtotal, company.currency_id, company, date)
                total[1] += qty
                total[2] += subtotal
            for product, (cost, qty, subtotal) in totals.items():
                order._set_product_cost(product, cost / qty, subtotal / qty)

    def _set_product_cost(self, product, new_cost, order_price):
        self.ensure_one()
        company = self.company_id
        product = product.with_company(company).sudo()
        old_cost = product.standard_price
        vals = {
            'po_cost_order_id': self.id,
            'po_cost_date': fields.Datetime.now(),
            'po_cost_price': order_price,
            'po_cost_currency_id': self.currency_id.id,
        }
        changed = float_compare(old_cost, new_cost, precision_digits=self.env[
            'decimal.precision'].precision_get('Product Price')) != 0
        if changed:
            vals['standard_price'] = new_cost
        # sudo: with automated inventory valuation a cost change books a
        # revaluation entry, which a purchase user may not be allowed to create.
        product.write(vals)
        if changed:
            body = _(
                "Cost updated from %(old)s to %(new)s by purchase order %(order)s.",
                old=company.currency_id.format(old_cost),
                new=company.currency_id.format(new_cost),
                order=Markup(self._get_html_link()),
            )
            product.product_tmpl_id.message_post(body=body)

#EoF
