# Alignment Decision
- Decision: Override stock.move._action_done (not _action_assign)
- Rationale: _action_done is the final confirmation step. Checking here
  ensures NO move can result in negative stock, regardless of how it was
  created (manual, MRP, automated).
- Alternative considered: Override _action_assign — but this only runs
  for some move types, not all.
