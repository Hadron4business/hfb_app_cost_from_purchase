# -*- coding: utf-8 -*-
# vim: tabstop=4 softtabstop=0 shiftwidth=4 smarttab expandtab fileformat=unix
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
{
    'name': "Product Cost from Purchase Orders",
    'summary': "Confirming a purchase order updates the product cost with the price you actually paid",
    'description': """
Product Cost from Purchase Orders
=================================

Margins on quotations, sales orders and reports are computed from the product
Cost field. When nobody updates it, the margins are fiction.

With this app, every confirmed purchase order writes the purchase price into
the Cost of its products (products using the Standard Price costing method):

* the price is net of discounts and taxes,
* converted to the product unit of measure and to the company currency,
* several lines of the same product are averaged by quantity,
* the product keeps the last order, date and original price,
* the change is logged in the product chatter.

Products costed with FIFO or Average Cost are skipped - Odoo already updates
their cost on receipt. The feature can be switched off per company in the
Purchase settings.
""",
    'version': "17.0.1.0.0",
    'author': "Hadron for Business sp. z o.o.",
    'website': "http://hadronforbusiness.com",
    'license': "OPL-1",
    'category': "Inventory/Purchase",
    'depends': [
        'purchase',
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/product_views.xml',
    ],
    'images': [
        'static/description/banner_screenshot.png',
    ],
    'installable': True,
    'application': False,
}
