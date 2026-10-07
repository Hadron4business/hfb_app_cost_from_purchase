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

	Product Cost from Purchase Orders - products
	Per-company trace of the purchase order that last set the product cost
	(order, date, original price and currency), shown on the product form when
	the product has a single variant.
"""
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    po_cost_order_id = fields.Many2one(
        'purchase.order', string="Cost Set by Order", company_dependent=True, copy=False,
        help="Last confirmed purchase order that updated the cost of this product.")
    po_cost_date = fields.Datetime(
        string="Cost Updated On", company_dependent=True, copy=False)
    po_cost_price = fields.Float(
        string="Order Price", company_dependent=True, copy=False, digits='Product Price',
        help="Unit price paid on that order, in the order currency and the "
             "product unit of measure, net of discounts and taxes.")
    po_cost_currency_id = fields.Many2one(
        'res.currency', string="Order Currency", company_dependent=True, copy=False)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    po_cost_order_id = fields.Many2one(
        'purchase.order', string="Cost Set by Order", compute='_compute_po_cost')
    po_cost_date = fields.Datetime(string="Cost Updated On", compute='_compute_po_cost')
    po_cost_price = fields.Float(
        string="Order Price", compute='_compute_po_cost', digits='Product Price')
    po_cost_currency_id = fields.Many2one(
        'res.currency', string="Order Currency", compute='_compute_po_cost')

    @api.depends_context('company')
    @api.depends('product_variant_ids')
    def _compute_po_cost(self):
        for template in self:
            variant = template.product_variant_ids if len(template.product_variant_ids) == 1 else False
            template.po_cost_order_id = variant.po_cost_order_id if variant else False
            template.po_cost_date = variant.po_cost_date if variant else False
            template.po_cost_price = variant.po_cost_price if variant else 0.0
            template.po_cost_currency_id = variant.po_cost_currency_id if variant else False

#EoF
