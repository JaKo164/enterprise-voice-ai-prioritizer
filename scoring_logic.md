# Scoring Logic

This tool supports enterprise AI discovery by making prioritization transparent and repeatable.

## Scoring dimensions (1-5)

- **Business Value** (higher is better): expected impact on revenue, cost, CX, risk posture, or productivity.
- **Implementation Effort** (lower is better): engineering and delivery effort needed.
- **Data Readiness** (higher is better): quality, accessibility, and coverage of required data.
- **Integration Complexity** (lower is better): effort/risk of integrating with existing systems.
- **Compliance/Risk** (lower is better): regulatory, legal, security, and reputational risk.
- **Executive Sponsorship** (higher is better): leadership alignment and ability to unblock delivery.
- **Time to Value** (lower is better): speed to first measurable business outcome.

## Weighting model

Weights are chosen to reflect a practical enterprise strategy lens:

- Business Value: **25%**
- Implementation Effort: **15%**
- Data Readiness: **15%**
- Integration Complexity: **10%**
- Compliance/Risk: **10%**
- Executive Sponsorship: **15%**
- Time to Value: **10%**

For dimensions where lower is better, the app inverts the raw 1-5 score during normalization.

## Weighted Priority Score

The app calculates a weighted average on normalized scores (1-5).
A higher score indicates a better candidate for near-term prioritization.

## Quick-win vs Strategic-bet view

The app also computes two derived indicators:

- **Feasibility Score**: average of implementation ease/speed/risk-related dimensions plus data readiness.
- **Strategic Potential**: average of business value, sponsorship, and readiness.

These two indicators are plotted to help teams classify use cases as:

- Quick Win
- Strategic Bet
- Quick Win + Strategic
- Longer-Term Candidate

This helps portfolio discussions move from opinion-driven to criteria-driven decisions.
