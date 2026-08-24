# Data Flow
1. User attempts to validate a stock move (click "Check Availability" or "Validate")
2. Odoo calls stock.move._action_done()
3. Our override intercepts: checks available qty via stock.quant
4. If available < requested: create el.stock.alert + send email + raise UserError
5. If available >= requested: call super()._action_done() (normal flow)
