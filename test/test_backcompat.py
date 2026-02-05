from __future__ import annotations

from datetime import datetime, timezone

from metaspn_schemas.core import SignalEnvelope


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
