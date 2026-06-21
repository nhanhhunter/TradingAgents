# Exec Plan

## Goal

Make prompted credentials reusable across supported local and container
execution modes without reading or mutating unrelated ancestor files.

## Scope

In scope:

- Environment-file resolution, loading, and persistence.
- Provider and VNstock prompts.
- Docker named-volume wiring.
- Documentation and automated regression tests.

Out of scope:

- OS keychain integration.
- Live provider calls.
- Automatic credential migration.

## Risk Classification

Risk flags:

- Audit/security.
- External systems.
- Existing behavior.
- Cross-platform.

Hard gates:

- Credential handling.
- External provider configuration.

## Work Phases

1. Reproduce ancestor-file mutation.
2. Define deterministic resolution.
3. Add failing regression tests.
4. Implement shared resolver.
5. Wire Docker persistence.
6. Verify focused and full test suites.

## Stop Conditions

Pause if the fix would expose secrets, weaken environment-variable precedence,
or require deleting/migrating user files.
