# Alignment Decision - el_commission_type

## Design Decisions

### Decision 1: Computed Name Field
**Decision:** Use computed field with store=True
**Rationale:** 
- Ensures consistency (name always matches type + percentage)
- Stored for search/filter performance
- Read-only prevents user errors

### Decision 2: Selection Field for Team Type
**Decision:** Use Selection instead of Many2one
**Rationale:**
- Limited, stable set of options
- No need for user customization
- Simpler UI and better performance

### Decision 3: Standalone Menu
**Decision:** Create top-level Commissions menu
**Rationale:**
- Clear separation of concerns
- Easy to find
- Room for future expansion (batches, reports, etc.)