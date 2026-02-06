from __future__ import annotations

from datetime import datetime, timezone

from metaspn_schemas import (
    FailureLabel,
    GateCalibrationRecommendation,
    LearningOutcomeWindow,
    PolicyOverrideReview,
)
from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION

NOW = datetime(2026, 2, 6, 18, 0, tzinfo=timezone.utc)


def assert_round_trip(instance: object, cls: type) -> None:
    payload = instance.to_dict()
    rebuilt = cls.from_dict(payload)
    assert rebuilt == instance


def test_round_trip_m3_learning_contracts() -> None:
    outcome = LearningOutcomeWindow(
        window_id="lw_1",
        entity_id="ent_1",
        attempted_at=NOW,
        window_start=NOW,
        window_end=NOW,
        outcome="reply_received",
        success=True,
        metrics={"reply_latency_hours": 3.5},
    )
    failure = FailureLabel(
        label_id="fl_1",
        entity_id="ent_1",
        category="delivery",
        code="EMAIL_BOUNCE",
        evidence="SMTP 550",
        labeled_at=NOW,
        metadata={"provider": "ses"},
    )
    recommendation = GateCalibrationRecommendation(
        recommendation_id="gcr_1",
        gate_name="email_gate",
        created_at=NOW,
        threshold_delta=-0.05,
        cooldown_seconds_delta=3600,
        confidence=0.81,
        rationale="Decrease threshold to recover recall.",
        based_on_windows=("w2", "w1"),
    )
    review = PolicyOverrideReview(
        review_id="por_1",
        recommendation_id="gcr_1",
        decision="approved",
        reviewed_at=NOW,
        reviewer="ops@metaspn",
        reason="Matches observed drift.",
        applied_threshold_delta=-0.04,
    )

    assert_round_trip(outcome, LearningOutcomeWindow)
    assert_round_trip(failure, FailureLabel)
    assert_round_trip(recommendation, GateCalibrationRecommendation)
    assert_round_trip(review, PolicyOverrideReview)


def test_m3_deterministic_serialization_and_defaults() -> None:
    failure = FailureLabel(
        label_id="fl_1",
        entity_id="ent_1",
        category="delivery",
        code="EMAIL_BOUNCE",
        evidence="SMTP 550",
        labeled_at=NOW,
        metadata={"z": "2", "a": "1"},
    )
    recommendation = GateCalibrationRecommendation(
        recommendation_id="gcr_1",
        gate_name="email_gate",
        created_at=NOW,
        threshold_delta=-0.05,
        cooldown_seconds_delta=3600,
        confidence=0.81,
        rationale="Decrease threshold.",
        based_on_windows=("w2", "w1"),
    )

    failure_data = failure.to_dict()
    rec_data = recommendation.to_dict()

    assert failure_data["schema_version"] == DEFAULT_SCHEMA_VERSION
    assert list(failure_data["metadata"].keys()) == ["a", "z"]
    assert rec_data["based_on_windows"] == ["w1", "w2"]
    assert rec_data["created_at"] == "2026-02-06T18:00:00Z"
