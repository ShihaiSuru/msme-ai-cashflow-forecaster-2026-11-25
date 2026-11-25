#!/usr/bin/env python3
"""
MSME AI Cash Flow Forecaster — Starter Script
==========================================

Practical demo for Indian MSMEs:
- Loads sample invoice data (INR, GST-aware)
- Applies realistic payment cycle heuristics
- Projects cash position over 90 days
- Estimates working capital buffer
- Highlights shortfall risks

Uses only Python standard library. Designed to be readable,
extensible, and useful as a foundation for real tooling.
"""

from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict

# ---------------------------------------------------------------------------
# Configuration & Heuristics (Indian MSME context)
# ---------------------------------------------------------------------------
class ForecastConfig:
    STARTING_CASH = 250_000          # ₹
    FORECAST_DAYS = 90
    GST_CASH_LAG_DAYS = 15           # Approximate time to claim ITC / net GST impact
    BUFFER_PERCENT = 0.15            # Extra buffer as % of projected outflows
    MIN_BUFFER = 50_000              # Floor buffer in ₹

    # Average collection days by customer segment (common MSME experience)
    PAYMENT_DAYS = {
        "retail": 25,
        "b2b": 52,
        "government": 75,
        "export": 40,
    }

    # Simple operating outflow assumption (rent, salaries, utilities, materials)
    MONTHLY_OPERATING_OUTFLOW = 180_000


# ---------------------------------------------------------------------------
# Sample Invoice Data (replace with real CSV later)
# ---------------------------------------------------------------------------
SAMPLE_INVOICES = [
    {"id": "INV-001", "date": "2026-11-01", "amount": 180_000, "gst_rate": 0.18, "customer_type": "b2b", "status": "open"},
    {"id": "INV-002", "date": "2026-11-05", "amount": 95_000, "gst_rate": 0.18, "customer_type": "retail", "status": "open"},
    {"id": "INV-003", "date": "2026-11-10", "amount": 320_000, "gst_rate": 0.18, "customer_type": "b2b", "status": "open"},
    {"id": "INV-004", "date": "2026-11-15", "amount": 65_000, "gst_rate": 0.05, "customer_type": "retail", "status": "open"},
    {"id": "INV-005", "date": "2026-11-20", "amount": 450_000, "gst_rate": 0.18, "customer_type": "government", "status": "open"},
    {"id": "INV-006", "date": "2026-11-22", "amount": 120_000, "gst_rate": 0.18, "customer_type": "b2b", "status": "open"},
    {"id": "INV-007", "date": "2026-10-15", "amount": 210_000, "gst_rate": 0.18, "customer_type": "export", "status": "paid"},  # already collected
]


def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")


def expected_collection_date(invoice: Dict, config: ForecastConfig) -> datetime:
    """Calculate expected cash receipt date based on customer type."""
    invoice_date = parse_date(invoice["date"])
    days = config.PAYMENT_DAYS.get(invoice["customer_type"], 45)
    return invoice_date + timedelta(days=days)


def build_cash_flow_events(invoices: List[Dict], config: ForecastConfig) -> Dict[datetime, float]:
    """
    Build a daily net cash movement map.
    Positive = inflow, Negative = outflow.
    """
    events = defaultdict(float)
    today = datetime(2026, 11, 25)  # Fixed for reproducible demo

    # Inflows from open invoices
    for inv in invoices:
        if inv["status"] != "open":
            continue
        collect_date = expected_collection_date(inv, config)
        if collect_date.date() >= today.date():
            # Net amount after GST (simplified — actual cash is base + GST collected)
            base = inv["amount"]
            gst = base * inv["gst_rate"]
            net_inflow = base + gst
            events[collect_date] += net_inflow

    # Regular operating outflows (spread evenly)
    daily_op = config.MONTHLY_OPERATING_OUTFLOW / 30
    for day_offset in range(config.FORECAST_DAYS):
        d = today + timedelta(days=day_offset)
        events[d] -= daily_op

    # Simplified GST cash impact lag (net payable/refund approximation)
    # In a real tool this would come from GSTR data
    gst_lag_date = today + timedelta(days=config.GST_CASH_LAG_DAYS)
    events[gst_lag_date] -= 45_000  # illustrative net GST outflow

    return events


def generate_forecast(config: ForecastConfig, invoices: List[Dict]):
    events = build_cash_flow_events(invoices, config)
    today = datetime(2026, 11, 25)

    cash = config.STARTING_CASH
    shortfall_days = []
    daily_positions = []

    total_inflows = 0.0
    total_outflows = 0.0

    for day_offset in range(config.FORECAST_DAYS):
        current_day = today + timedelta(days=day_offset)
        net = events.get(current_day, 0.0)
        cash += net

        if net > 0:
            total_inflows += net
        else:
            total_outflows += abs(net)

        daily_positions.append((current_day, cash))

        if cash < 0:
            shortfall_days.append((current_day, cash))

    # Working capital buffer recommendation
    buffer = max(config.MIN_BUFFER, total_outflows * config.BUFFER_PERCENT)
    recommended_buffer = round(buffer, -3)  # nearest thousand

    return {
        "starting_cash": config.STARTING_CASH,
        "total_inflows": round(total_inflows),
        "total_outflows": round(total_outflows),
        "ending_cash": round(cash),
        "shortfall_days": shortfall_days,
        "recommended_buffer": recommended_buffer,
        "daily_positions": daily_positions,
    }


def print_report(result: Dict):
    print("=" * 60)
    print(" MSME AI Cash Flow Forecast (Next 90 Days)")
    print("=" * 60)
    print(f"Starting cash:          ₹{result['starting_cash']:,}")
    print(f"Expected inflows:       ₹{result['total_inflows']:,}")
    print(f"Expected outflows:      ₹{result['total_outflows']:,}")
    print(f"Projected ending cash:  ₹{result['ending_cash']:,}")
    print()

    if result["shortfall_days"]:
        print(f"⚠️  Shortfall days detected: {len(result['shortfall_days'])}")
        for day, bal in result["shortfall_days"][:5]:
            print(f"   • {day.strftime('%Y-%m-%d')}: ₹{bal:,.0f}")
        if len(result["shortfall_days"]) > 5:
            print(f"   ... and {len(result['shortfall_days']) - 5} more")
    else:
        print("✅ No shortfall days in the forecast period.")

    print()
    print(f"Recommended working capital buffer: ₹{result['recommended_buffer']:,}")
    print()
    print("Insights:")
    print("  • B2B customers average ~52 days — prioritize follow-ups here.")
    print("  • Government invoices take longest; consider factoring or partial advances.")
    print("  • Maintain at least the recommended buffer to absorb GST timing & delays.")
    print("=" * 60)


def main():
    config = ForecastConfig()
    result = generate_forecast(config, SAMPLE_INVOICES)
    print_report(result)

    # Optional: write simple CSV of daily positions
    try:
        with open("cashflow_forecast.csv", "w") as f:
            f.write("date,projected_cash\n")
            for day, cash in result["daily_positions"]:
                f.write(f"{day.strftime('%Y-%m-%d')},{cash:.0f}\n")
        print("\n📊 Daily positions written to cashflow_forecast.csv")
    except Exception as e:
        print(f"(Could not write CSV: {e})")


if __name__ == "__main__":
    main()
