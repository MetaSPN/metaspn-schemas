from __future__ import annotations

from datetime import datetime, timezone

from metaspn_schemas import (
    CreatorBehaviorCorrelation,
    PromiseEvaluated,
    PromisePredictiveAccuracy,
    PromiseRegistered,
    TokenHealthScoreCard,
    TokenOutcomeObserved,
    TokenOutcomeWindow,
    TokenSignalSeen,
)
from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION

NOW = datetime(2026, 2, 6, 22, 0, tzinfo=timezone.utc)


def assert_round_trip(instance: object, cls: type) -> None:
    payload = instance.to_dict()
    rebuilt = cls.from_dict(payload)
    assert rebuilt == instance


def test_round_trip_token_promise_contracts() -> None:
    signal = TokenSignalSeen("ts_1", "tok_1", "cr_1", "mention", NOW)
    registered = PromiseRegistered("pr_1", "tok_1", "cr_1", NOW, "Ship by Friday")
    evaluated = PromiseEvaluated("pe_1", "pr_1", "tok_1", NOW, "kept", 0.89)
    health = TokenHealthScoreCard("th_1", "tok_1", NOW, 0.8, 0.2, 0.7)
    observed = TokenOutcomeObserved("to_1", "tok_1", NOW, "reply", True, value=1.0)
    window = TokenOutcomeWindow(
        "tw_1", "tok_1", NOW, NOW, NOW, 0.65, outcomes=("no_reply", "reply")
    )
    predictive = PromisePredictiveAccuracy("ppa_1", "pr_1", NOW, 0.77, 42)
    correlation = CreatorBehaviorCorrelation(
        "cbc_1", "cr_1", NOW, "posting_frequency", "promise_kept", 0.31
    )

    assert_round_trip(signal, TokenSignalSeen)
    assert_round_trip(registered, PromiseRegistered)
    assert_round_trip(evaluated, PromiseEvaluated)
    assert_round_trip(health, TokenHealthScoreCard)
    assert_round_trip(observed, TokenOutcomeObserved)
    assert_round_trip(window, TokenOutcomeWindow)
    assert_round_trip(predictive, PromisePredictiveAccuracy)
    assert_round_trip(correlation, CreatorBehaviorCorrelation)


def test_token_promise_deterministic_ordering_and_defaults() -> None:
    signal = TokenSignalSeen(
        "ts_1", "tok_1", "cr_1", "mention", NOW, metadata={"z": "2", "a": "1"}
    )
    window = TokenOutcomeWindow(
        "tw_1", "tok_1", NOW, NOW, NOW, 0.65, outcomes=("z", "a"), metrics={"z": 2.0, "a": 1.0}
    )

    signal_data = signal.to_dict()
    window_data = window.to_dict()

    assert signal_data["schema_version"] == DEFAULT_SCHEMA_VERSION
    assert list(signal_data["metadata"].keys()) == ["a", "z"]
    assert window_data["outcomes"] == ["a", "z"]
    assert list(window_data["metrics"].keys()) == ["a", "z"]
