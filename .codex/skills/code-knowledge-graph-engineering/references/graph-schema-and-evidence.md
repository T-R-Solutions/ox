# Evidence-bearing graph schema

A design record for an edge can include id, source_node, target_node, relation_type, evidence_class, snapshot, source_range, producer_version and evidence_locator. Define which fields are required per edge class. Reject a resolved call without resolution evidence rather than accepting a boolean verified flag supplied by an inference producer.

The [W3C PROV data model](https://www.w3.org/TR/prov-dm/) distinguishes entities, activities and agents. It is a useful vocabulary for attributing an extraction to inputs and a producer; this skill does not require RDF or PROV conformance.

Two independent producers can disagree. Keep their claims separate with source identities and a conflict state; do not collapse them into one stronger claim. A path from file A to B through inferred edges is exploratory context, not proof that changing A breaks B. State the allowed evidence classes in every impact query.
