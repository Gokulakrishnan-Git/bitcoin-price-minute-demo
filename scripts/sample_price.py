#!/usr/bin/env python3
"""Sample Coinbase BTC/USD spot price on a fixed one-minute cadence."""

import csv
import json
import os
import time
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
    samples = int(os.getenv("SAMPLES", "5"))
    interval = int(os.getenv("INTERVAL_SECONDS", "60"))
    ROOT.joinpath("data").mkdir(exist_ok=True)

    if not HISTORY_PATH.exists():
        with HISTORY_PATH.open("w", newline="", encoding="utf-8") as history:
            csv.writer(history).writerow(["timestamp_utc", "currency", "price", "source"])

    summary_lines = [
        "## Bitcoin price samples",
        "",
        "| Sample | Time (UTC) | Price |",
        "|---:|---|---:|",
    ]
    summary_file = os.getenv("GITHUB_STEP_SUMMARY")

    for index in range(samples):
        started = time.monotonic()
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

        line = f"| {index + 1} | {timestamp} | {amount} {currency} |"
        summary_lines.append(line)
        print(f"Sample {index + 1}/{samples}: {timestamp} — {amount} {currency}")

        if index + 1 < samples:
            time.sleep(max(0, interval - (time.monotonic() - started)))

    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as summary:
            summary.write("\n".join(summary_lines) + "\n")


if __name__ == "__main__":
    main()
