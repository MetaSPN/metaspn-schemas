# Changelog

All notable changes to this project will be documented in this file.

## [0.8.0] - 2026-02-06

- Added token/promise schema contracts:
  `TokenSignalSeen`, `PromiseRegistered`, `PromiseEvaluated`,
  `TokenHealthScoreCard`, `TokenOutcomeObserved`, `TokenOutcomeWindow`,
  `PromisePredictiveAccuracy`, and `CreatorBehaviorCorrelation`.
- Added explicit `NoReply` schema support alongside `NoReplyObserved`.
- Exported new contracts from top-level package surface.
- Added serde + backcompat tests for token/promise and no-reply payloads.
- Bumped default schema version to `0.8`.

## [0.7.0] - 2026-02-06

- Added `NoReplyObserved` outcome schema for synthetic/manual no-reply demo signals.
- Added focused demo contract test coverage spanning ingestion, profile/score/route,
  recommendation artifacts, outcomes, and learning-loop records.
- Added backcompat default tests for `NoReplyObserved`.
- Bumped default schema version to `0.7`.

## [0.6.0] - 2026-02-06

- Added M3 learning contracts:
  `LearningOutcomeWindow`, `FailureLabel`,
  `GateCalibrationRecommendation`, and `PolicyOverrideReview`.
- Exported new M3 contracts from top-level `metaspn_schemas` package surface.
- Added round-trip, deterministic-ordering, and backcompat tests for M3 payload variants.
- Bumped default schema version to `0.6`.

## [0.5.0] - 2026-02-06

- Added M2 recommendation contracts:
  `Recommendation`, `DailyDigestEntry`, `DraftMessage`, and `ApprovalOverride`.
- Exported new M2 contracts from top-level `metaspn_schemas` package surface.
- Added round-trip and backcompat tests for M2 payload variants.
- Bumped default schema version to `0.5`.

## [0.4.0] - 2026-02-06

- Added canonical M1 contracts:
  `M1ProfileEnrichment`, `M1ScoreCard`, and `M1RoutingRecommendation`.
- Exported M1 contracts from top-level `metaspn_schemas` import surface.
- Normalized feature payload datetimes to UTC for deterministic, timezone-safe serialization.
- Added M1 tests for round-trip serde, deterministic dict ordering, and backcompat defaults.
- Bumped default schema version to `0.4`.

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
