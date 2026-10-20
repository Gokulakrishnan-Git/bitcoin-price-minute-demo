#!/usr/bin/env python3
"""Fetch one Coinbase BTC/USD spot price for this scheduled run."""

import csv
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_URL = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
ROOT = Path(__file__).resolve().parents[1]
LATEST_PATH = ROOT / "data" / "latest.json"
HISTORY_PATH = ROOT / "data" / "prices.csv"


def fetch_price():
    request = urllib.request.Request(
        API_URL,
        headers={"Accept": "application/json", "User-Agent": "bitcoin-price-minute-demo"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.load(response)
    data = payload["data"]
    return data["amount"], data["currency"]


def main():
    ROOT.joinpath("data").mkdir(exist_ok=True)
    if not HISTORY_PATH.exists():
        with HISTORY_PATH.open("w", newline="", encoding="utf-8") as history:
            csv.writer(history).writerow(["timestamp_utc", "currency", "price", "source"])

    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    amount, currency = fetch_price()
    record = {
        "timestamp_utc": timestamp,
        "pair": f"BTC-{currency}",
        "price": amount,
        "source": API_URL,
    }

    with HISTORY_PATH.open("a", newline="", encoding="utf-8") as history:
        csv.writer(history).writerow([timestamp, currency, amount, API_URL])
    LATEST_PATH.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    print(f"Bitcoin price at {timestamp}: {amount} {currency}", flush=True)
    summary_file = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as summary:
            summary.write(
                "## Bitcoin price\n\n"
                "| Time (UTC) | Price |\n|---|---:|\n"
                f"| {timestamp} | {amount} {currency} |\n"
            )


if __name__ == "__main__":
    main()
