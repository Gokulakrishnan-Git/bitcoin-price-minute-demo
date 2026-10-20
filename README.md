# Bitcoin Price Every Five Minutes

A small GitHub Actions demo that fetches Coinbase's public BTC/USD spot price once every five minutes.

## How it works

The workflow is scheduled with `*/5 * * * *`. Each run fetches one price, then updates:

- [Latest reading](data/latest.json)
- [Price history](data/prices.csv)

The run's **Summary** shows that single reading. You can also request one reading manually from **Actions → Bitcoin price every 5 minutes → Run workflow**. GitHub may delay scheduled runs, so they may not start exactly on the five-minute mark.

## Data source

The script uses Coinbase's public spot-price endpoint. Prices are informational and can differ from exchange execution prices.

## Permissions

The workflow uses the repository's built-in GITHUB_TOKEN with write access to repository contents so it can commit updated price data. No API key or other secret is needed.
