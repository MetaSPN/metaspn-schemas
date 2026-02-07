from __future__ import annotations

from datetime import datetime, timedelta, timezone

from metaspn_schemas import (
    AttentionScoreUpdate,
    FounderStakeView,
    GameAccountView,
    PlayerAccountView,
    RewardClaim,
    RewardProjection,
    SeasonAccountView,
    StakeAccountView,
    parse_attention_score_update,
    parse_reward_projection,
    parse_season1_payload,
    validate_reward_claim,
    validate_season1_payload,
)
from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION

NOW = datetime(2026, 2, 7, 16, 0, tzinfo=timezone.utc)
LOCAL_NOW = datetime(2026, 2, 7, 8, 0, tzinfo=timezone(timedelta(hours=-8)))


def assert_round_trip(instance: object, cls: type) -> None:
    payload = instance.to_dict()
    rebuilt = cls.from_dict(payload)
    assert rebuilt == instance


def test_round_trip_season1_contracts() -> None:
    season = SeasonAccountView(
        season_id=1,
        authority="auth_1",
        towel_mint="mint_1",
        active=True,
        started_at=NOW,
        reward_pool_total=1_000,
        reward_pool_remaining=900,
        total_staked=500,
        founder_locked_total=100,
    )
    game = GameAccountView(season_id=1, game_id=101, attention_score_bps=7200)
    stake = StakeAccountView(owner="player_1", season_id=1, game_id=101, amount=200, active=True)
    player = PlayerAccountView(
        owner="player_1",
        season_id=1,
        issued_towel_balance=800,
        staked_towel=200,
        claimed_rewards=0,
        has_claimed=False,
    )
    founder = FounderStakeView(owner="founder_1", season_id=1, amount=100, active=True)
    attention = AttentionScoreUpdate(
        season_id=1,
        game_id=101,
        attention_score_bps=7300,
        updated_at=NOW,
        updated_by="admin_1",
    )
    projection = RewardProjection(
        projection_id="rp_1",
        owner="player_1",
        season_id=1,
        projected_at=NOW,
        staked_towel=200,
        total_staked=500,
        reward_pool_total=1_000,
        reward_pool_remaining=900,
        projected_payout=400,
    )
    claim = RewardClaim(
        claim_id="rc_1",
        owner="player_1",
        season_id=1,
        claimed_at=NOW,
        amount=360,
        status="claimed",
    )

    assert_round_trip(season, SeasonAccountView)
    assert_round_trip(game, GameAccountView)
    assert_round_trip(stake, StakeAccountView)
    assert_round_trip(player, PlayerAccountView)
    assert_round_trip(founder, FounderStakeView)
    assert_round_trip(attention, AttentionScoreUpdate)
    assert_round_trip(projection, RewardProjection)
    assert_round_trip(claim, RewardClaim)


def test_season1_utc_normalization_and_deterministic_serialization() -> None:
    attention = AttentionScoreUpdate(
        season_id=1,
        game_id=101,
        attention_score_bps=8100,
        updated_at=LOCAL_NOW,
        metadata={"z": "2", "a": "1"},
    )
    projection = RewardProjection(
        projection_id="rp_2",
        owner="player_2",
        season_id=1,
        projected_at=LOCAL_NOW,
        staked_towel=50,
        total_staked=1_000,
        reward_pool_total=5_000,
        reward_pool_remaining=4_000,
        projected_payout=200,
        metadata={"z": "2", "a": "1"},
    )

    attention_data = attention.to_dict()
    projection_data = projection.to_dict()

    assert attention_data["updated_at"] == "2026-02-07T16:00:00Z"
    assert projection_data["projected_at"] == "2026-02-07T16:00:00Z"
    assert list(attention_data["metadata"].keys()) == ["a", "z"]
    assert list(projection_data["metadata"].keys()) == ["a", "z"]
    assert attention_data["schema_version"] == DEFAULT_SCHEMA_VERSION


def test_season1_parse_and_validate_helpers() -> None:
    parsed_attention = parse_attention_score_update(
        {
            "seasonId": 1,
            "gameId": 44,
            "attentionScoreBps": 5400,
            "updatedAt": "2026-02-07T16:00:00Z",
            "updatedBy": "admin_1",
        }
    )
    assert isinstance(parsed_attention, AttentionScoreUpdate)

    parsed_projection = parse_reward_projection(
        {
            "projectionId": "rp_3",
            "owner": "player_3",
            "seasonId": 1,
            "computedAt": "2026-02-07T16:00:00Z",
            "stakedAmount": 120,
            "totalStaked": 1200,
            "rewardPoolTotal": 2400,
            "rewardPoolRemaining": 2400,
            "projectedPayout": 240,
        }
    )
    assert parsed_projection.projection_id == "rp_3"

    parsed_generic = parse_season1_payload(
        "SeasonAccountView",
        {
            "seasonId": 1,
            "authorityPubkey": "auth_1",
            "towelMint": "mint_1",
            "active": True,
            "startTs": 1762502400,
        },
    )
    assert isinstance(parsed_generic, SeasonAccountView)

    is_valid, errors = validate_season1_payload(
        "RewardClaim",
        {
            "claimId": "rc_2",
            "owner": "player_2",
            "seasonId": 1,
            "claimedAt": "2026-02-07T16:00:00Z",
            "amount": 100,
            "status": "claimed",
        },
    )
    assert is_valid
    assert errors == ()

    invalid, claim_errors = validate_reward_claim(
        {
            "claimId": "",
            "owner": "",
            "seasonId": 0,
            "claimedAt": "2026-02-07T16:00:00Z",
            "amount": -1,
            "status": "unknown",
        }
    )
    assert not invalid
    assert claim_errors
