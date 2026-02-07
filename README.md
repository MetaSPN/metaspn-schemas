# metaspn-schemas

Canonical, stdlib-only schema package for MetaSPN-compatible systems.

## Install

```bash
pip install metaspn-schemas
```

## Development

```bash
python -m pip install -e .[dev]
pytest -q
python -m build
python -m twine check dist/*
```

## Design constraints

- Tiny and dependency-light (stdlib only)
- Frozen dataclasses for immutable-by-default objects
- Explicit `schema_version` on all public objects
- `to_dict()` / `from_dict()` on every schema
- UTC ISO-8601 datetime serialization
- Traceability metadata (`trace_id`, `caused_by`, provenance)
- Privacy mode support (`to_dict(privacy_mode=True)` omits raw blobs)

## Example

```python
from datetime import timezone, datetime

from metaspn_schemas import SignalEnvelope
from metaspn_schemas.utils.ids import generate_id

signal = SignalEnvelope(
    signal_id=generate_id("signal"),
    timestamp=datetime.now(timezone.utc),
    source="linkedin.webhook",
    payload_type="SocialPostSeen",
    payload={"post_id": "123", "platform": "linkedin"},
    schema_version="0.9",
)

as_dict = signal.to_dict()
round_trip = SignalEnvelope.from_dict(as_dict)
```

## Public imports

```python
from metaspn_schemas import (
    SignalEnvelope,
    EmissionEnvelope,
    Task,
    Result,
    SocialPostSeen,
    ProfileEnriched,
    ScoresComputed,
    StateMachineConfig,
    GateTransitionAttempt,
    OutcomeWindowEvaluation,
    CalibrationRecord,
    FailureTaxonomyRecord,
    M1ProfileEnrichment,
    M1ScoreCard,
    M1RoutingRecommendation,
    Recommendation,
    DailyDigestEntry,
    DraftMessage,
    ApprovalOverride,
    NoReplyObserved,
    NoReply,
    TokenSignalSeen,
    PromiseRegistered,
    PromiseEvaluated,
    TokenHealthScoreCard,
    TokenOutcomeObserved,
    TokenOutcomeWindow,
    PromisePredictiveAccuracy,
    CreatorBehaviorCorrelation,
    SeasonAccountView,
    GameAccountView,
    StakeAccountView,
    PlayerAccountView,
    FounderStakeView,
    AttentionScoreUpdate,
    RewardProjection,
    RewardClaim,
    LearningOutcomeWindow,
    FailureLabel,
    GateCalibrationRecommendation,
    PolicyOverrideReview,
    parse_state_machine_config,
    validate_state_machine_config,
    parse_season1_payload,
    validate_season1_payload,
)
```

## Contract Surfaces

`v0.2.0` adds canonical shared contracts for gate/state-machine coordination:

- `StateMachineConfig` + `StateTransitionRule` for static machine configuration payloads.
- `GateTransitionAttempt` for transition snapshot records.
- `OutcomeWindowEvaluation` for downstream learning/evaluation windows.
- `CalibrationRecord` + `FailureTaxonomyRecord` for calibration/failure taxonomy telemetry.

Parse/validate hooks exposed at package top-level:

- `parse_state_machine_config(payload)` for current + prior minor payload shape normalization.
- `validate_state_machine_config(config_or_payload)` returning `(is_valid, errors)`.

Versioning expectations:

- Additive fields/types are backwards compatible and ship in minor bumps.
- Renames/type changes are breaking and require major bumps.
- Each record carries `schema_version` for replay/backcompat handling.

## Ingestion Contracts

`v0.3.0` adds M0 ingestion + resolver handoff schemas:

- `RawSocialPostSeenEvent`
Required: `event_id`, `source`, `seen_at`, `raw`.
Optional: `resolver_handoff`.
- `NormalizedSocialPostSeenEvent`
Required: `event_id`, `source`, `platform`, `post_id`, `author_handle`, `content`, `seen_at`.
Optional: `post_url`, `topics`, `resolver_handoff`.
- `IngestionParseErrorEvent`
Required: `error_id`, `source`, `occurred_at`, `error_type`, `message`.
Optional: `raw_payload`, `resolver_handoff`.
- `ResolverHandoff`
Required: `handoff_id`, `entity_ref`, `provenance_source`, `provenance_step`, `attached_at`.
Optional provenance metadata: `metadata`.

All ingestion timestamps are normalized to UTC on construction and serde output remains deterministic.

## M1 Profile/Score/Route Contracts

`v0.4.0` adds canonical M1 payloads for profile enrichment, scoring, and routing:

- `M1ProfileEnrichment`
Required: `enrichment_id`, `entity_id`, `enriched_at`, `role`, `organization`, `topics`, `evidence_summary`.
Optional metadata: `metadata`.
- `M1ScoreCard`
Required: `score_id`, `entity_id`, `computed_at`, `fit`, `quality`, `reply_likelihood`, `scorer`.
Optional scorer metadata: `scorer_metadata`.
- `M1RoutingRecommendation`
Required: `recommendation_id`, `entity_id`, `recommended_at`, `playbook`, `rationale`, `priority`, `suggested_action`.
Optional metadata: `metadata`.

All M1 timestamps are normalized to UTC and dict outputs are serialized deterministically.

## M2 Recommendation Contracts

`v0.5.0` adds canonical recommendation and human-approval artifacts:

- `Recommendation`
Required: `recommendation_id`, `entity_id`, `playbook`, `score`, `rationale`, `priority`, `created_at`.
Optional metadata: `metadata`.
- `DailyDigestEntry`
Required: `digest_entry_id`, `entity_id`, `rank`, `action_item`, `created_at`.
Optional metadata: `metadata`.
- `DraftMessage`
Required: `draft_id`, `entity_id`, `channel`, `body`, `tone`, `created_at`.
Optional: `subject`, `constraints`, `metadata`.
- `ApprovalOverride`
Required: `approval_id`, `draft_id`, `status`, `reason`, `reviewed_at`.
Optional: `edited_subject`, `edited_body`, `reviewer`, `metadata`.

All M2 timestamps are normalized to UTC and serialization remains deterministic.

## M3 Learning Contracts

`v0.6.0` adds canonical learning-loop artifacts:

- `LearningOutcomeWindow`
Required: `window_id`, `entity_id`, `attempted_at`, `window_start`, `window_end`, `outcome`, `success`.
Optional: `metrics`.
- `FailureLabel`
Required: `label_id`, `entity_id`, `category`, `code`, `evidence`, `labeled_at`.
Optional: `metadata`.
- `GateCalibrationRecommendation`
Required: `recommendation_id`, `gate_name`, `created_at`, `threshold_delta`, `cooldown_seconds_delta`, `confidence`, `rationale`.
Optional: `based_on_windows`, `metadata`.
- `PolicyOverrideReview`
Required: `review_id`, `recommendation_id`, `decision`, `reviewed_at`, `reviewer`, `reason`.
Optional: `applied_threshold_delta`, `applied_cooldown_seconds_delta`, `metadata`.

All M3 timestamps are normalized to UTC and list/dict outputs are deterministic.

## Demo Contract Subset

`v0.7.0` verifies a canonical demo path across stages:

- Ingestion/social: `NormalizedSocialPostSeenEvent`
- Profile/scoring/routing: `M1ProfileEnrichment`, `M1ScoreCard`, `M1RoutingRecommendation`
- Recommendation artifacts: `Recommendation`, `DailyDigestEntry`, `DraftMessage`
- Outcomes: `NoReplyObserved` (synthetic/manual no-reply support), plus existing message/reply outcomes
- Learning loop: `LearningOutcomeWindow`, `FailureLabel`, `GateCalibrationRecommendation`

Focused demo serde tests ensure this subset runs without ad hoc payload classes.

## Token/Promise Contracts

`v0.8.0` adds canonical token/promise lifecycle contracts:

- `TokenSignalSeen`
- `PromiseRegistered`
- `PromiseEvaluated`
- `TokenHealthScoreCard`
- `TokenOutcomeObserved`
- `TokenOutcomeWindow`
- `PromisePredictiveAccuracy`
- `CreatorBehaviorCorrelation`
- `NoReply` (explicit alias-style no-reply schema support in addition to `NoReplyObserved`)

These contracts use deterministic dict serialization and UTC-normalized timestamps.

## Season 1 Contracts

`v0.9.0` adds canonical Season 1 account/reward contracts:

- `SeasonAccountView`
- `GameAccountView`
- `StakeAccountView`
- `PlayerAccountView`
- `FounderStakeView`
- `AttentionScoreUpdate`
- `RewardProjection`
- `RewardClaim`

Season 1 parser/validator hooks exposed at package top-level:

- `parse_season1_payload(payload_type, payload)` for canonical payload parsing.
- `validate_season1_payload(payload_type, payload_or_obj)` returning `(is_valid, errors)`.

Per-type parse/validate helpers are also exported for targeted consumers and tests.

## Package layout

```text
metaspn-schemas/
  pyproject.toml
  README.md
  src/metaspn_schemas/
    __init__.py
    core.py
    tasks.py
    entities.py
    social.py
    outcomes.py
    token_promises.py
    recommendations.py
    learning.py
    features.py
    ingestion.py
    state_machine.py
    state_fragments.py
    utils/
      ids.py
      time.py
      serde.py
  test/
    test_serde.py
    test_ids.py
    test_backcompat.py
    test_ingestion.py
    test_m1_contracts.py
    test_m2_contracts.py
    test_m3_learning_contracts.py
    test_token_promises.py
    test_demo_contracts.py
    test_state_machine.py
```

## Release

Release automation is configured in:

- `.github/workflows/ci.yml`
- `.github/workflows/publish.yml`

See `RELEASE.md` for the end-to-end push + PyPI release flow.
