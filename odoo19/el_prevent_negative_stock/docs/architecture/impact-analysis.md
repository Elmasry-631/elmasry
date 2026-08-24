# Impact Analysis
- stock.move: extended via _inherit, _action_done overridden
- No new fields on stock.move (no DB impact)
- No changes to existing views
- New model el.stock.alert (new table)
- New mail.template for notifications
- Performance: one extra stock.quant query per move validation
