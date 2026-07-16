# Alignment Decision — ie_stock_movement_report

## Alignment with Odoo 19 best practices

| Decision point                  | Choice                                  | Rationale                                      |
|---------------------------------|-----------------------------------------|------------------------------------------------|
| Security pattern                | ir.module.privilege (not category)      | LAW 11/14 — Odoo 19 native                     |
| View tag                        | `<list>` (not `<tree>`)                 | LAW 6 — Odoo 17+ deprecation                   |
| Conditional visibility          | `invisible=` (not `attrs=`)             | LAW 6 — Odoo 17+ deprecation                   |
| res.groups category_id          | Omitted                                 | E-VER-020 — removed in Odoo 18+                |
| QWeb structure                  | t-foreach between html_container + external_layout | LAW 19 — Odoo 19 pattern            |
| QWeb field rendering            | `t-options` (not `t-field-options`)     | LAW 19 — Odoo 19 deprecation                   |
| QWeb variable name              | `o.` (not `object.`)                    | LAW 19 — Odoo 19 convention                    |
| Table cell content              | wrapped in `<span>`                     | LAW 19 — wkhtmltopdf rendering reliability     |
| Module name prefix              | `ie_`                                   | LAW 13 — Ibrahim Elmasry author convention     |
| Manifest data[] order           | security → wizard → reports → views → menu | LAW 16 — load order critical                |
| Performance strategy            | batch fetch + in-memory                 | Spec requirement for thousands of moves       |
| Cost source                     | product.standard_price                  | stock_account Community — no Enterprise dep   |

## Trade-offs

| Trade-off                            | Choice                | Why                                           |
|--------------------------------------|-----------------------|-----------------------------------------------|
| AbstractModel vs TransientModel for report logic | AbstractModel | No persisted records; pure data provider      |
| Single template file vs split        | Single template file  | Report + paperformat together — easier to find |
| _() in Python vs QWeb-only           | Both                  | Wizard strings need _() too                   |

## Future considerations

- If FIFO/LIFO valuation is needed later, add stock_account_pond (Enterprise)
  dependency and switch cost source from standard_price to valuation layer
