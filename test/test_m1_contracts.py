from __future__ import annotations

from datetime import datetime, timezone

from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION
from metaspn_schemas.features import M1ProfileEnrichment, M1RoutingRecommendation, M1ScoreCard
from metaspn_schemas import (
    M1ProfileEnrichment as RootM1ProfileEnrichment,
    M1RoutingRecommendation as RootM1RoutingRecommendation,
    M1ScoreCard as RootM1ScoreCard,
)

NOW = datetime(2026, 2, 6, 12, 0, tzinfo=timezone.utc)


def assert_round_trip(instance: object, cls: type) -> None:
    data = instance.to_dict()
    rebuilt = cls.from_dict(data)
    assert rebuilt == instance


def test_round_trip_m1_contracts() -> None:
    profile = M1ProfileEnrichment(
        enrichment_id="m1p_1",
        entity_id="ent_1",
        enriched_at=NOW,
        role="Head of Sales",
        organization="Acme",
        topics=("outbound", "ai"),
        evidence_summary="Role and org inferred from profile + posts.",
        metadata={"source": "worker.m1"},
    )
    scores = M1ScoreCard(
        score_id="m1s_1",
        entity_id="ent_1",
        computed_at=NOW,
        fit=0.84,
        quality=0.78,
        reply_likelihood=0.67,
        scorer="m1-v2",
        scorer_metadata={"model": "xgboost", "dataset": "m1_2026_02"},
    )
    route = M1RoutingRecommendation(
        recommendation_id="m1r_1",
        entity_id="ent_1",
        recommended_at=NOW,
        playbook="warm_outbound",
        rationale="High fit and positive intent signals.",
        priority=1,
        suggested_action="send_intro_message",
        metadata={"owner": "ops"},
    )

    assert_round_trip(profile, M1ProfileEnrichment)
    assert_round_trip(scores, M1ScoreCard)
    assert_round_trip(route, M1RoutingRecommendation)


def test_m1_defaults_and_deterministic_ordering() -> None:
    scores = M1ScoreCard(
        score_id="m1s_1",
        entity_id="ent_1",
        computed_at=NOW,
        fit=0.84,
        quality=0.78,
        reply_likelihood=0.67,
        scorer="m1-v2",
        scorer_metadata={"z": "2", "a": "1"},
    )

    data = scores.to_dict()
    assert data["schema_version"] == DEFAULT_SCHEMA_VERSION
    assert list(data["scorer_metadata"].keys()) == ["a", "z"]


def test_m1_contracts_are_exposed_at_package_root() -> None:
    assert RootM1ProfileEnrichment is M1ProfileEnrichment
    assert RootM1ScoreCard is M1ScoreCard
    assert RootM1RoutingRecommendation is M1RoutingRecommendation
