# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-02-05

- Initial release of `metaspn-schemas`.
- Added immutable envelope schemas: `SignalEnvelope`, `EmissionEnvelope`.
- Added task contracts: `Task`, `Result`.
- Added shared payload modules: social, outcomes, entities, features.
- Added state fragments: identity, evidence, scores, cooldowns, attempts.
- Added stdlib-only serialization helpers with `to_dict()` / `from_dict()`.
- Added UTC ISO-8601 datetime handling and deterministic dict ordering.
- Added privacy-mode serialization behavior for raw payload omission.
- Added test suite for serde, IDs, and backward compatibility.
