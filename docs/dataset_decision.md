# Dataset decision

**Selected for v1.0.0:** US Treasury daily par yield curves (nominal and real) and bill rates, 1990 to the build cutoff.

Why: official primary source; genuinely daily time series; no credentials; unambiguous redistribution position (US Government work, see licensing doc); small enough to ship in full; one coherent semantic family (market-observed yields on US Treasuries).

Why not the others: FRED forbids redistribution (rejected); SEC market-structure and EDGAR data are redistributable but heterogeneous and larger, better as follow-on datasets.

Unresolved uncertainties: Treasury publishes no explicit data licence on the pages we could reach (the privacy/site-policy URLs returned 404); we rely on 17 U.S.C. §105. Treasury may revise historic values; v1 is a snapshot (see spec).
