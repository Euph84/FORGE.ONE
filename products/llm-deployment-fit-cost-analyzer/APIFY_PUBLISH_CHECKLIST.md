# APIFY CONSOLE — V0.3 PUBLISH CHECKLIST

1. Pricing model: Pay per event.
2. Keep synthetic `apify-actor-start` enabled at its default price.
3. REMOVE synthetic `apify-default-dataset-item`.
4. Custom event: `analysis-completed`.
5. Initial validation price: USD 0.25 per completed analysis.
6. Memory: actor.json caps the run at 256 MB.
7. Set a sensible minimum max-total-charge before public launch.
8. Run one private paid-event test and verify exactly one result item, exactly one `analysis-completed` charge, no dataset-item charge, and immediate termination.
9. Only then publish to Store.

NO LIVE GPU PRICE CLAIMS IN V0.3.
NO CUSTOMER CREDENTIALS.
NO DEPLOYMENT MUTATIONS.
