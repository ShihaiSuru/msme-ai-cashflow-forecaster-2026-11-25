# MSME AI Cash Flow Forecaster

**Practical AI-assisted cash flow forecasting and working capital estimation for Indian MSMEs.**

![Status](https://img.shields.io/badge/status-starter-brightgreen) ![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![Focus](https://img.shields.io/badge/focus-MSME%20fintech-orange)

## The Problem

Indian MSMEs (Micro, Small and Medium Enterprises) are the backbone of the economy, contributing significantly to GDP, employment, and exports. Yet they face chronic cash flow challenges:

- Over ₹8.1 trillion locked in delayed payments (Ministry of MSME reports).
- Irregular payment cycles from large buyers (30–90+ days).
- GST compliance overhead and input tax credit timing issues.
- Limited access to affordable working capital tools — most solutions are either too expensive, too complex, or bank-centric.
- Manual spreadsheet tracking that fails to predict shortfalls early.

Result: business owners spend excessive time chasing receivables instead of growing the business, and many miss growth opportunities due to liquidity gaps.

## The Solution

**msme-ai-cashflow-forecaster** is a lightweight, transparent Python starter that helps MSME founders and finance teams:

1. Ingest simple invoice data (date, amount, GST rate, customer type, expected payment days).
2. Apply realistic Indian MSME heuristics (average collection periods, GST cash impact, seasonal adjustments).
3. Generate a 90-day cash flow forecast highlighting potential shortfalls.
4. Estimate minimum working capital buffer needed to stay liquid.
5. Surface actionable insights (e.g., “focus collections on Category A customers” or “consider invoice discounting for next 30 days”).

It is designed as an open, educational, and extensible foundation — not a black-box SaaS. You can run it locally, extend the logic, or integrate with real data sources (Tally, GST portals, UPI statements, Account Aggregator) later.

## Features (Starter Version)

- Sample Indian MSME invoice dataset (INR, 18% GST common rate).
- Payment cycle modeling by customer segment (retail / B2B / government).
- Simple rolling cash flow projection with shortfall alerts.
- Working capital requirement estimator.
- Clear console output and optional CSV export.
- Fully commented code for easy customization.

## Quick Start

### Prerequisites
- Python 3.8 or higher
- No external dependencies for the starter (uses only standard library)

### Run the demo
```bash
git clone https://github.com/ShihaiSuru/msme-ai-cashflow-forecaster-2026-11-25.git
cd msme-ai-cashflow-forecaster-2026-11-25
python cashflow_forecaster.py
```

You will see a 90-day forecast summary, identified liquidity gaps, and a recommended working capital buffer.

### Customize
Edit the `SAMPLE_INVOICES` list or load your own CSV. Adjust heuristics in the `ForecastConfig` class (payment days, GST cash lag, buffer percentage).

## Example Output
```
=== MSME Cash Flow Forecast (Next 90 Days) ===
Starting cash: ₹250,000
Expected inflows: ₹1,845,000
Expected outflows (GST + operating): ₹1,120,000
Projected ending cash: ₹975,000
Shortfall days detected: 2 (Day 18, Day 42)
Recommended working capital buffer: ₹185,000
Insight: Accelerate collections from B2B customers (avg 52 days).
```

## Roadmap Ideas
- CSV / Excel upload
- Integration with GSTN / e-invoice data
- UPI transaction reconciliation module
- Simple ML model for payment probability (scikit-learn)
- Dashboard (Streamlit)
- Multi-currency / multi-state GST support

## Why This Exists

Built as a public demonstration of practical, founder-led fintech tooling focused on Indian MSMEs. The goal is to show clear problem understanding, clean implementation, and openness for collaboration — rather than another closed demo.

## License

MIT License — free to use, modify, and extend.

## Author

**ShihaiSuru**  
Building fintech tools that help Indian MSMEs manage cash flow with clarity and AI assistance.

---

*This is a starter/educational project. Always validate financial models with your CA or finance professional before making business decisions.*
