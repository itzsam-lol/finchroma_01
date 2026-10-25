# Licensing and attribution

| Component | Licence / status | Evidence |
|---|---|---|
| Source data (US Treasury rates) | US Government work; works of the federal government are not subject to US copyright (17 U.S.C. §105) | Treasury interest-rate pages carry no copyright claim or restrictive terms; sampled 2026-10-25. Treasury's dedicated site-policy URLs returned 404, so no explicit licence text was retrieved. |
| FinChrona compiled dataset (reshaping, schema, reports) | CC0 1.0 | We assert no rights beyond the public-domain source; CC0 is chosen to make that explicit. |
| Code and documentation | MIT (`LICENSE`) | Repository owner's licence file |

Residual uncertainty: the lack of an explicit Treasury licence statement. Outside the US, rights in US Government works may differ; users should verify for their jurisdiction.

Attribution requested (not legally required): "Source: U.S. Department of the Treasury, Daily Treasury Rates; compiled by FinChrona." No Treasury endorsement is implied; Treasury seals and logos are not used.

Retrieval conduct: public CSV endpoints only, no authentication or access controls bypassed, identified User-Agent, 1 s delay between requests.

Not used: FRED/ALFRED (terms prohibit caching/redistribution), SEC and EDGAR data (not part of v1; sec.gov permits copying with citation).
