# Design

## Domain Model

An environment-file resolver selects one primary credential file from an
explicit override, an exact workspace file, or the per-user configuration
directory. Parent-directory discovery is forbidden.

## Application Flow

Package startup loads deterministic files without replacing non-empty process
environment values. Credential prompts persist through the same resolver and
immediately update the current process.

## Interface Contract

`TRADINGAGENTS_ENV_FILE` explicitly selects the primary file. Relative values
are relative to the launch directory. Prompt messages report the resolved
destination but never the key.

## Data Model

Credential files remain dotenv text files. Updates preserve unrelated entries.
New files request owner-only permissions where supported.

## UI / Platform Impact

Source checkouts use `.env`. Installed commands use
`~/.tradingagents/.env`. Docker uses
`/home/appuser/.tradingagents/.env` on the existing named volume.

## Observability

The CLI prints only the environment-variable name and destination path.

## Alternatives Considered

1. Always use the current directory. Rejected because installed commands may
   run from arbitrary or unwritable directories and container writes vanish.
2. Always use the user directory. Rejected because it would unexpectedly stop
   updating existing source-checkout `.env` files.
3. Keep `find_dotenv`. Rejected because parent search caused the defect.
