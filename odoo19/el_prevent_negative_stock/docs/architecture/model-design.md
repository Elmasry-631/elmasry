# Model Design — el_prevent_negative_stock

## stock.move extension

Override `_action_done()` to intercept before any stock move is confirmed:
1. For each move, calculate available quantity = on-hand qty at source location
2. If move would result in negative quantity → raise UserError
3. Create el.stock.alert record with details
4. Send email to warehouse manager

## el.stock.alert (new model)
- Read-only log model
- Inherits mail.thread for chatter
- Sequence-based name (AL/2026/00001)
- Records all rejected negative stock attempts

## Key logic in _action_done override:
```python
for move in self:
    if move.state in ('done', 'cancel'):
        continue
    available = self.env['stock.quant']._get_available_quantity(
        move.product_id, move.location_id
    )
    if available < move.quantity:
        # Create alert
        alert = self.env['el.stock.alert'].create({...})
        # Send email
        template.send_mail(alert.id)
        # Reject
        raise UserError(_(
            'Insufficient stock for %s at %s: requested %s, available %s'
        ) % (move.product_id.name, move.location_id.name,
             move.quantity, available))
```
