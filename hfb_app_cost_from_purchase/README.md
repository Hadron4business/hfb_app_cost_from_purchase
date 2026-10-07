# Product Cost from Purchase Orders

Confirming a purchase order writes the price paid into the Cost of its products (products using the Standard Price costing method).

## What it does

- **Automatic** - The cost is updated the moment a purchase order is confirmed - also after a manager approval.
- **Real net price** - Discounts are taken into account, taxes are not. Converted to the product unit of measure and the company currency.
- **Several lines, one product** - When a product appears on several lines of one order, the cost is the quantity-weighted average.
- **Traceable** - The product shows which order set its cost, when, and the original price and currency. Every change is logged in the chatter.
- **Safe for valuation** - FIFO and Average Cost products are skipped - Odoo updates them on receipt. Free lines never wipe the cost.
- **Per company** - Switch it on or off for each company in the Purchase settings.

## How to use it

1. Install the app. The option Update Product Cost from Purchase Orders in Purchase > Configuration > Settings is on by default.
2. Make sure your products use the Standard Price costing method (product category, Inventory Valuation section - visible with the Inventory app).
3. Confirm a purchase order. The Cost of its products is updated.
4. Open a product: the Purchase tab shows the order that set the cost, the date and the price paid; the chatter keeps the history.

## Good to know

- With automated inventory valuation, a cost change on a product in stock creates the usual revaluation entry, exactly as a manual change of the cost would.
- Lines with a zero price (free goods, samples) are ignored.
- Cancelling a purchase order does not restore the previous cost.
- The trace fields are kept per company and per product variant.

## Technical

- Depends only on `purchase`; when `stock_account` is installed, only products with cost method `standard` are updated.
- Hook point: `purchase.order.button_approve` (called by `button_confirm` and by the manager approval).
- Override `purchase.order._cost_is_updatable(product)` to change which products are updated.

## Status

Odoo 18 build. Tested on the Odoo.sh test instances (automated RPC tests and manual tests, 2026-10-07). Icon and banner included - ready for publication.
