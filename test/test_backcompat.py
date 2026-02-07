from __future__ import annotations

from datetime import datetime, timezone

from metaspn_schemas.core import SignalEnvelope
from metaspn_schemas.features import M1ProfileEnrichment, M1RoutingRecommendation, M1ScoreCard
from metaspn_schemas.ingestion import NormalizedSocialPostSeenEvent, RawSocialPostSeenEvent
from metaspn_schemas.learning import GateCalibrationRecommendation, PolicyOverrideReview
from metaspn_schemas.outcomes import NoReply, NoReplyObserved
from metaspn_schemas.recommendations import ApprovalOverride, DraftMessage
from metaspn_schemas.season1 import parse_reward_claim, parse_season_account_view
from metaspn_schemas.state_machine import parse_state_machine_config
from metaspn_schemas.token_promises import PromiseRegistered, TokenSignalSeen


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


def test_m2_backcompat_prior_minor_payload_defaults() -> None:
    legacy_draft = {
        "draft_id": "drf_legacy",
        "entity_id": "ent_1",
        "channel": "email",
        "body": "hello",
        "tone": "professional",
        "created_at": "2026-02-06T15:00:00Z",
        "schema_version": "0.4",
    }
    legacy_approval = {
        "approval_id": "apr_legacy",
        "draft_id": "drf_legacy",
        "status": "approved",
        "reason": "looks fine",
        "reviewed_at": "2026-02-06T15:00:00Z",
        "schema_version": "0.4",
    }

    draft = DraftMessage.from_dict(legacy_draft)
    approval = ApprovalOverride.from_dict(legacy_approval)

    assert draft.subject is None
    assert draft.constraints == ()
    assert draft.metadata == {}
    assert approval.edited_subject is None
    assert approval.edited_body is None
    assert approval.reviewer is None
    assert approval.metadata == {}


def test_m3_backcompat_prior_minor_payload_defaults() -> None:
    legacy_recommendation = {
        "recommendation_id": "gcr_legacy",
        "gate_name": "email_gate",
        "created_at": "2026-02-06T18:00:00Z",
        "threshold_delta": -0.05,
        "cooldown_seconds_delta": 3600,
        "confidence": 0.8,
        "rationale": "legacy payload without windows",
        "schema_version": "0.5",
    }
    legacy_review = {
        "review_id": "por_legacy",
        "recommendation_id": "gcr_legacy",
        "decision": "approved",
        "reviewed_at": "2026-02-06T18:00:00Z",
        "reviewer": "ops@metaspn",
        "reason": "looks good",
        "schema_version": "0.5",
    }

    recommendation = GateCalibrationRecommendation.from_dict(legacy_recommendation)
    review = PolicyOverrideReview.from_dict(legacy_review)

    assert recommendation.based_on_windows == ()
    assert recommendation.metadata == {}
    assert review.applied_threshold_delta is None
    assert review.applied_cooldown_seconds_delta is None
    assert review.metadata == {}


def test_demo_no_reply_backcompat_defaults() -> None:
    legacy_payload = {
        "no_reply_id": "nr_legacy",
        "message_id": "msg_1",
        "observed_at": "2026-02-06T20:00:00Z",
        "wait_hours": 72,
        "schema_version": "0.6",
    }

    no_reply = NoReplyObserved.from_dict(legacy_payload)
    assert no_reply.reason == "timeout"
    assert no_reply.metadata == {}


def test_no_reply_backcompat_defaults() -> None:
    legacy_payload = {
        "no_reply_id": "nr_legacy_2",
        "message_id": "msg_2",
        "observed_at": "2026-02-06T20:00:00Z",
        "wait_hours": 48,
        "schema_version": "0.7",
    }
    no_reply = NoReply.from_dict(legacy_payload)
    assert no_reply.reason == "timeout"
    assert no_reply.metadata == {}


def test_token_promise_backcompat_prior_minor_payload_defaults() -> None:
    legacy_signal = {
        "token_signal_id": "ts_legacy",
        "token_id": "tok_1",
        "creator_id": "cr_1",
        "signal_type": "mention",
        "seen_at": "2026-02-06T22:00:00Z",
        "schema_version": "0.7",
    }
    legacy_registered = {
        "promise_id": "pr_legacy",
        "token_id": "tok_1",
        "creator_id": "cr_1",
        "registered_at": "2026-02-06T22:00:00Z",
        "promise_text": "Ship by Friday",
        "schema_version": "0.7",
    }

    signal = TokenSignalSeen.from_dict(legacy_signal)
    registered = PromiseRegistered.from_dict(legacy_registered)

    assert signal.metadata == {}
    assert registered.source is None
    assert registered.metadata == {}


def test_season1_backcompat_chain_alias_payloads() -> None:
    legacy_season = {
        "seasonId": 1,
        "authorityPubkey": "auth_legacy",
        "towelMint": "mint_legacy",
        "active": True,
        "startTs": 1762502400,
        "endTs": 1765180800,
        "rewardPoolTotal": 1000,
        "rewardPoolRemaining": 800,
        "totalStaked": 400,
        "founderLockedTotal": 100,
        "schema_version": "0.8",
    }
    legacy_claim = {
        "claimId": "rc_legacy",
        "owner": "player_legacy",
        "seasonId": 1,
        "claimedAt": "2026-02-07T16:00:00Z",
        "amount": 200,
        "status": "claimed",
        "tx_sig": "abc123",
        "schema_version": "0.8",
    }

    season = parse_season_account_view(legacy_season)
    claim = parse_reward_claim(legacy_claim)

    assert season.season_id == 1
    assert season.authority == "auth_legacy"
    assert season.towel_mint == "mint_legacy"
    assert season.started_at == datetime(2025, 11, 7, 8, 0, tzinfo=timezone.utc)
    assert season.ended_at == datetime(2025, 12, 8, 8, 0, tzinfo=timezone.utc)
    assert season.reward_pool_total == 1000
    assert claim.claim_id == "rc_legacy"
    assert claim.transaction_signature == "abc123"
