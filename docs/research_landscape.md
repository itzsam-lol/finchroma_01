# Research landscape (inspected 2026-10-25)

Candidates evaluated against official pages. "Redistribution" is the decisive criterion for a public release.

| Candidate | Data / frequency | Access | Redistribution evidence | Verdict |
|---|---|---|---|---|
| A. SEC market structure data (MIDAS) | Per-security, per-exchange, decile and quote-life metrics; zip packages, last updated June 2026; spreads/depth file covers 2013 only | Public download | sec.gov privacy page: information on sec.gov "is considered public information and may be copied or further distributed"; asks for citation | Redistributable, but heterogeneous schemas, mixed frequencies and partial history; larger build effort. Good candidate for a later release |
| B. FRED / ALFRED | Thousands of macro series, vintages | API key required | FRED legal page: no storing/caching/archiving or bulk download; no ML training; many series carry third-party copyright | **Rejected** (cannot lawfully republish) |
| C. SEC EDGAR APIs (filings, XBRL facts) | Event-based, quarterly/annual statements | Public, requires User-Agent, rate limit 10 req/s | Same sec.gov reuse statement | Feasible and valuable, but large, definition-heavy; planned for a later release |
| D. US Treasury daily rates (par nominal, par real, bill rates) | Daily, nominal 1990-, real 2003/04-, bills 2002- | Public CSV per year, no key | US Government work; see `licensing_and_attribution.md` for the residual uncertainty | **Selected** |
| E. Treasury FiscalData APIs | Average interest rates, debt, auctions | Public API | FiscalData states its data is public domain | Candidate for future expansion |

Sources: https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics ; https://www.sec.gov/data-research/market-structure-data ; https://www.sec.gov/about/privacy-information ; https://fred.stlouisfed.org/legal/ ; https://www.sec.gov/search-filings/edgar-application-programming-interfaces
