# Architecture Inventories — el_prevent_negative_stock

## Model Inventory

### 1. el.stock.alert (NEW)
| Field | Type | Options |
|-------|------|---------|
| name | Char | required, default=sequence |
| product_id | Many2one(product.product) | required, index=True |
| location_id | Many2one(stock.location) | required, index=True |
| requested_qty | Float | required |
| available_qty | Float | required |
| move_id | Many2one(stock.move) | |
| user_id | Many2one(res.users) | default=lambda self: self.env.user |
| state | Selection | [('rejected','Rejected')] |
| company_id | Many2one(res.company) | default=lambda self: self.env.company |

Methods: none (read-only model)

### 2. stock.move (EXTENSION via _inherit)
| Override Method | Purpose |
|----------------|---------|
| _action_done | Check available qty before confirming. If negative → raise UserError + create alert + send email |

## View Inventory
| View ID | Type | Model |
|---------|------|-------|
| view_el_stock_alert_list | list | el.stock.alert |
| view_el_stock_alert_form | form | el.stock.alert |
| view_el_stock_alert_search | search | el.stock.alert |
| action_el_stock_alert | action | el.stock.alert |

## Button → Method Map
No buttons (read-only alert model)

## State Machine
No state machine (alert is always 'rejected')
