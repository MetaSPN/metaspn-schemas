from __future__ import annotations

from datetime import datetime, timezone

from metaspn_schemas import (
    DailyDigestEntry,
    DraftMessage,
    FailureLabel,
    GateCalibrationRecommendation,
    LearningOutcomeWindow,
    M1ProfileEnrichment,
    M1RoutingRecommendation,
    M1ScoreCard,
    NoReplyObserved,
    NormalizedSocialPostSeenEvent,
    Recommendation,
)

NOW = datetime(2026, 2, 6, 20, 0, tzinfo=timezone.utc)


def assert_round_trip(instance: object, cls: type) -> None:
    data = instance.to_dict()
    rebuilt = cls.from_dict(data)
    assert rebuilt == instance


def test_demo_contract_subset_round_trip() -> None:
    signal = NormalizedSocialPostSeenEvent(
        event_id="demo_sig_1",
        source="demo.io",
        platform="linkedin",
        post_id="p1",
        author_handle="@demo",
        content="Looking for outbound help",
        seen_at=NOW,
        topics=("outbound", "ai"),
    )
    profile = M1ProfileEnrichment(
        enrichment_id="demo_prof_1",
        entity_id="ent_1",
        enriched_at=NOW,
        role="Head of Sales",
        organization="Acme",
        topics=("ai", "outbound"),
        evidence_summary="Profile + posts",
    )
    score = M1ScoreCard(
        score_id="demo_score_1",
        entity_id="ent_1",
        computed_at=NOW,
        fit=0.82,
        quality=0.74,
        reply_likelihood=0.58,
        scorer="m1",
    )
    routed = M1RoutingRecommendation(
        recommendation_id="demo_route_1",
        entity_id="ent_1",
        recommended_at=NOW,
        playbook="warm_outbound",
        rationale="Good fit",
        priority=1,
        suggested_action="draft_email",
    )
    recommendation = Recommendation(
        recommendation_id="demo_rec_1",
        entity_id="ent_1",
        playbook="warm_outbound",
        score=0.8,
        rationale="quality + fit",
        priority=1,
        created_at=NOW,
    )
    digest = DailyDigestEntry(
        digest_entry_id="demo_dig_1",
        entity_id="ent_1",
        rank=1,
        action_item="Send intro email",
        created_at=NOW,
    )
    draft = DraftMessage(
        draft_id="demo_drf_1",
        entity_id="ent_1",
        channel="email",
        body="Hi there...",
        tone="professional",
        created_at=NOW,
    )
    no_reply = NoReplyObserved("demo_nr_1", "m1", NOW, 72)
    outcome_window = LearningOutcomeWindow(
        window_id="demo_win_1",
        entity_id="ent_1",
        attempted_at=NOW,
        window_start=NOW,
        window_end=NOW,
        outcome="no_reply",
        success=False,
    )
    failure = FailureLabel(
        label_id="demo_fail_1",
        entity_id="ent_1",
        category="engagement",
        code="NO_REPLY",
        evidence="No reply within SLA",
        labeled_at=NOW,
    )
    calibration = GateCalibrationRecommendation(
        recommendation_id="demo_cal_1",
        gate_name="email_gate",
        created_at=NOW,
        threshold_delta=-0.05,
        cooldown_seconds_delta=1800,
        confidence=0.79,
        rationale="restore recall",
    )

    assert_round_trip(signal, NormalizedSocialPostSeenEvent)
    assert_round_trip(profile, M1ProfileEnrichment)
    assert_round_trip(score, M1ScoreCard)
    assert_round_trip(routed, M1RoutingRecommendation)
    assert_round_trip(recommendation, Recommendation)
    assert_round_trip(digest, DailyDigestEntry)
    assert_round_trip(draft, DraftMessage)
    assert_round_trip(no_reply, NoReplyObserved)
    assert_round_trip(outcome_window, LearningOutcomeWindow)
    assert_round_trip(failure, FailureLabel)
    assert_round_trip(calibration, GateCalibrationRecommendation)


def test_demo_contract_deterministic_ordering() -> None:
    draft = DraftMessage(
        draft_id="demo_drf_1",
        entity_id="ent_1",
        channel="email",
        body="Hi there...",
        tone="professional",
        created_at=NOW,
        constraints=("z", "a"),
        metadata={"z": "2", "a": "1"},
    )
    no_reply = NoReplyObserved(
        no_reply_id="demo_nr_1",
        message_id="m1",
        observed_at=NOW,
        wait_hours=72,
        metadata={"z": "2", "a": "1"},
    )

    draft_data = draft.to_dict()
    no_reply_data = no_reply.to_dict()

    assert draft_data["constraints"] == ["a", "z"]
    assert list(draft_data["metadata"].keys()) == ["a", "z"]
    assert list(no_reply_data["metadata"].keys()) == ["a", "z"]
