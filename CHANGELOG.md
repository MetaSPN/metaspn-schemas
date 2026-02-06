# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2026-02-06

- Added ingestion contracts:
  `RawSocialPostSeenEvent`, `NormalizedSocialPostSeenEvent`,
  `IngestionParseErrorEvent`, and `ResolverHandoff`.
- Added top-level exports for new ingestion/resolver schemas.
- Added round-trip and backward-compatible serde tests for ingestion payload variants.
- Bumped default schema version to `0.3`.

## [0.2.0] - 2026-02-06

- Added state-machine contract schemas:
  `StateMachineConfig`, `StateTransitionRule`, `GateTransitionAttempt`,
  `OutcomeWindowEvaluation`, `CalibrationRecord`, and `FailureTaxonomyRecord`.
- Added public parser/validator entrypoints:
  `parse_state_machine_config` and `validate_state_machine_config`.
- Added backcompat normalization support for prior minor state-machine payload keys
  (`machine_id`, `machine_name`, `start_state`, `state_nodes`, `end_states`,
  and transition keys `from`/`to`/`event_name`).
- Added round-trip serde tests and validation tests for new contract objects.
- Bumped default schema version to `0.2`.

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
