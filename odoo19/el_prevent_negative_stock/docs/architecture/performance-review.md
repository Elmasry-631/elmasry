# Performance Review — el_prevent_negative_stock
N+1 Queries: 0 (single _get_available_quantity call per move)
Missing Indexes: 0 (product_id + location_id indexed)
Unbounded Queries: 0
Computed Field Chains: 0
Dashboard RPC Budget: N/A (no dashboard)
Verdict: PASS
