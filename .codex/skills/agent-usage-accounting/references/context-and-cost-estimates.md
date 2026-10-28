# Time, context and price

Specify intervals as [start, end) in an explicit reporting timezone. Convert event timestamps consistently and test midnight and daylight-saving boundaries where applicable. Late events may revise a period view while preserving the original observations and report version.

Context occupancy is a snapshot of an active request/window; daily token consumption is an accumulation. Neither implies task progress. Unknown context capacity or hidden agent messages prevent an exact occupancy percentage.

For cost, record tariff source, effective period, currency, per-unit denominator, cache categories and rounding. A local estimate can be useful if labeled; it is not a measured invoice. A missing tariff yields unknown cost even when tokens are measured. A partial total should display known cost plus unknown coverage, not a deceptively complete number. No live prices or provider subscriptions are assumed by this skill.
