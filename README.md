# Bitcoin Price Every Minute

A small GitHub Actions demo that samples Coinbase's public BTC/USD spot price once per minute.

## How it works

GitHub scheduled workflows run no more often than every five minutes. To demonstrate one-minute sampling, the workflow starts every five minutes and takes five readings about 60 seconds apart. GitHub can delay scheduled runs, so timing is approximate.

Each completed run updates:

- [Latest reading](data/latest.json)
- [Price history](data/prices.csv)

The run's **Summary** also lists all five readings. You can start a batch manually from **Actions → Bitcoin price every minute → Run workflow**.

## Data source

The script uses Coinbase's public spot-price endpoint. Prices are informational and can differ from exchange execution prices.

## Permissions

The workflow uses the repository's built-in GITHUB_TOKEN with write access to repository contents so it can commit updated price data. No API key or other secret is needed.
