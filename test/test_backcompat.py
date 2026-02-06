from __future__ import annotations

from datetime import datetime, timezone

from metaspn_schemas.core import SignalEnvelope
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
