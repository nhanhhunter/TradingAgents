# Cross-Platform API Key Persistence

## Status

implemented

## Current Behavior

The CLI can save prompted keys into an ancestor `.env`, and container-local
writes disappear when a container is replaced.

## Target Behavior

Loading and saving use one deterministic resolver. Source checkouts use their
own `.env`, installed commands use the user's TradingAgents configuration
directory, explicit paths are supported, and Docker writes to a named volume.

## Affected Users

- Interactive CLI users.
- Docker and Docker Compose users.
- Users installing the package on Linux, Windows, or macOS.

## Affected Product Docs

- `README.md`
- `docs/stories/US-002-first-run-api-key-prompts.md`

## Non-Goals

- Adding an operating-system keychain.
- Changing provider names or API-key environment variables.
- Migrating or deleting ancestor `.env` files automatically.
