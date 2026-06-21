# Cross-Platform API Key Persistence Design

## Problem

The CLI currently uses `find_dotenv(usecwd=True)` for both loading and saving
API keys. That search can walk above the current project and update an
unrelated ancestor `.env`. In Docker, writing to the image working directory
does not survive container replacement.

## Resolution Order

One shared resolver will determine the primary credential file:

1. `TRADINGAGENTS_ENV_FILE`, resolved relative to the current directory when
   necessary.
2. The exact current-directory `.env` when it already exists.
3. The exact current-directory `.env` when running from a TradingAgents source
   checkout.
4. `~/.tradingagents/.env` for installed-package use.

The resolver never searches parent directories.

## Loading

TradingAgents will load the resolved primary file and, when no explicit
override is configured, may use `~/.tradingagents/.env` as a fallback after an
exact current-directory `.env`.

Existing non-empty process environment variables remain authoritative. Empty
environment variables are treated as unset so Docker Compose entries such as
`OPENAI_API_KEY=` do not prevent a persisted value from loading.

The exact current-directory `.env.enterprise` remains supported without parent
directory search.

## Saving

Provider and VNstock prompts will call one persistence helper. The helper will:

- create the parent directory;
- create or update the resolved file without replacing unrelated entries;
- export the value into the current process;
- request owner-only file permissions where the operating system supports
  POSIX modes;
- report the exact destination without printing the secret.

## Platform Behavior

- Source checkout on Linux, macOS, or Windows: `<checkout>/.env`.
- Package installed and launched elsewhere: `~/.tradingagents/.env`.
- Explicit automation or CI: `TRADINGAGENTS_ENV_FILE`.
- Docker and Docker Compose:
  `/home/appuser/.tradingagents/.env`, persisted by the existing
  `tradingagents_data` named volume.
- Host-provided Docker/Compose environment variables continue to override
  stored values when they are non-empty.

## Compatibility

Provider-to-environment-variable mappings and prompt behavior do not change.
Existing exact current-directory `.env` files continue to work. Ancestor
`.env` discovery is intentionally removed because it can read or mutate
credentials belonging to another project.

## Validation

Automated tests will cover ancestor isolation, source checkout behavior,
installed-package fallback, explicit overrides, empty Docker-style environment
variables, persistence across process starts, VNstock reuse, and Dockerfile
wiring. Focused credential tests and the full pytest suite will be run.
