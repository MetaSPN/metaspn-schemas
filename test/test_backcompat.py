from __future__ import annotations

from datetime import datetime, timezone

from metaspn_schemas.core import SignalEnvelope
from metaspn_schemas.features import M1ProfileEnrichment, M1RoutingRecommendation, M1ScoreCard
from metaspn_schemas.ingestion import NormalizedSocialPostSeenEvent, RawSocialPostSeenEvent
from metaspn_schemas.state_machine import parse_state_machine_config


def test_signal_backcompat_prior_minor_payload() -> None:
    legacy_payload = {
        "signal_id": "s_legacy",
        "timestamp": "2025-01-01T10:30:00Z",
        "source": "legacy.source",
        "payload_type": "SocialPostSeen",
        "payload": {"post_id": "p1"},
        "schema_version": "0.0",
    }

    signal = SignalEnvelope.from_dict(legacy_payload)

    assert signal.signal_id == "s_legacy"
    assert signal.timestamp == datetime(2025, 1, 1, 10, 30, tzinfo=timezone.utc)
    assert signal.entity_refs == ()
    assert signal.trace is None
    assert signal.raw is None


def test_state_machine_backcompat_prior_minor_payload() -> None:
    legacy_payload = {
        "machine_id": "cfg_old",
        "machine_name": "default",
        "start_state": "seen",
        "state_nodes": ["seen", "queued", "sent"],
        "end_states": ["sent"],
        "transitions": [
            {"from": "seen", "to": "queued", "event_name": "route"},
            {"from": "queued", "to": "sent", "event_name": "dispatch"},
        ],
        "schema_version": "0.0",
    }

    config = parse_state_machine_config(legacy_payload)

    assert config.config_id == "cfg_old"
    assert config.machine_type == "default"
    assert config.initial_state == "seen"
    assert config.states == ("queued", "seen", "sent")
    assert config.terminal_states == ("sent",)
    assert config.transitions[0].from_state == "queued"
    assert config.transitions[0].event == "dispatch"


def test_raw_ingestion_backcompat_prior_minor_payload() -> None:
    legacy_payload = {
        "event_id": "raw_legacy",
        "source": "linkedin.webhook",
        "seen_at": "2026-01-15T09:00:00Z",
        "raw": {"id": "p1"},
        "schema_version": "0.2",
    }

    event = RawSocialPostSeenEvent.from_dict(legacy_payload)
    assert event.event_id == "raw_legacy"
    assert event.resolver_handoff is None
    assert event.seen_at == datetime(2026, 1, 15, 9, 0, tzinfo=timezone.utc)


def test_normalized_ingestion_backcompat_prior_minor_payload() -> None:
    legacy_payload = {
        "event_id": "norm_legacy",
        "source": "linkedin.webhook",
        "platform": "linkedin",
        "post_id": "p1",
        "author_handle": "@a",
        "content": "hello",
        "seen_at": "2026-01-15T09:00:00Z",
        "schema_version": "0.2",
    }

    event = NormalizedSocialPostSeenEvent.from_dict(legacy_payload)
    assert event.event_id == "norm_legacy"
    assert event.post_url is None
    assert event.topics == ()
    assert event.resolver_handoff is None


def test_m1_backcompat_prior_minor_payload_defaults() -> None:
    profile_payload = {
        "enrichment_id": "m1p_legacy",
        "entity_id": "ent_1",
        "enriched_at": "2026-02-06T12:00:00Z",
        "role": "Head of Sales",
        "organization": "Acme",
        "topics": ["ai", "outbound"],
        "evidence_summary": "legacy payload without metadata",
        "schema_version": "0.3",
    }
    score_payload = {
        "score_id": "m1s_legacy",
        "entity_id": "ent_1",
        "computed_at": "2026-02-06T12:00:00Z",
        "fit": 0.7,
        "quality": 0.6,
        "reply_likelihood": 0.5,
        "scorer": "legacy",
        "schema_version": "0.3",
    }
    route_payload = {
        "recommendation_id": "m1r_legacy",
        "entity_id": "ent_1",
        "recommended_at": "2026-02-06T12:00:00Z",
        "playbook": "warm_outbound",
        "rationale": "legacy payload without metadata",
        "priority": 2,
        "suggested_action": "send_intro_message",
        "schema_version": "0.3",
    }

    profile = M1ProfileEnrichment.from_dict(profile_payload)
    score = M1ScoreCard.from_dict(score_payload)
    route = M1RoutingRecommendation.from_dict(route_payload)

    assert profile.metadata == {}
    assert score.scorer_metadata == {}
    assert route.metadata == {}
