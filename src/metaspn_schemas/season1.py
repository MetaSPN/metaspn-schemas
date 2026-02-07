from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION
from metaspn_schemas.utils.serde import Serializable
from metaspn_schemas.utils.time import ensure_utc


@dataclass(frozen=True)
class SeasonAccountView(Serializable):
    season_id: int
    authority: str
    towel_mint: str
    active: bool
    started_at: datetime
    schema_version: str = DEFAULT_SCHEMA_VERSION
    ended_at: datetime | None = None
    reward_pool_total: int = 0
    reward_pool_remaining: int = 0
    total_staked: int = 0
    founder_locked_total: int = 0
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "started_at", ensure_utc(self.started_at))
        if self.ended_at is not None:
            object.__setattr__(self, "ended_at", ensure_utc(self.ended_at))


@dataclass(frozen=True)
class GameAccountView(Serializable):
    season_id: int
    game_id: int
    attention_score_bps: int
    schema_version: str = DEFAULT_SCHEMA_VERSION
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class StakeAccountView(Serializable):
    owner: str
    season_id: int
    game_id: int
    amount: int
    active: bool
    schema_version: str = DEFAULT_SCHEMA_VERSION
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class PlayerAccountView(Serializable):
    owner: str
    season_id: int
    issued_towel_balance: int
    staked_towel: int
    claimed_rewards: int
    has_claimed: bool
    schema_version: str = DEFAULT_SCHEMA_VERSION
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class FounderStakeView(Serializable):
    owner: str
    season_id: int
    amount: int
    active: bool
    schema_version: str = DEFAULT_SCHEMA_VERSION
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class AttentionScoreUpdate(Serializable):
    season_id: int
    game_id: int
    attention_score_bps: int
    updated_at: datetime
    schema_version: str = DEFAULT_SCHEMA_VERSION
    updated_by: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "updated_at", ensure_utc(self.updated_at))


@dataclass(frozen=True)
class RewardProjection(Serializable):
    projection_id: str
    owner: str
    season_id: int
    projected_at: datetime
    staked_towel: int
    total_staked: int
    reward_pool_total: int
    reward_pool_remaining: int
    projected_payout: int
    schema_version: str = DEFAULT_SCHEMA_VERSION
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "projected_at", ensure_utc(self.projected_at))


@dataclass(frozen=True)
class RewardClaim(Serializable):
    claim_id: str
    owner: str
    season_id: int
    claimed_at: datetime
    amount: int
    status: str
    schema_version: str = DEFAULT_SCHEMA_VERSION
    transaction_signature: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "claimed_at", ensure_utc(self.claimed_at))


SEASON1_PAYLOAD_PARSERS: dict[str, Any] = {
    "SeasonAccountView": lambda data: parse_season_account_view(data),
    "GameAccountView": lambda data: parse_game_account_view(data),
    "StakeAccountView": lambda data: parse_stake_account_view(data),
    "PlayerAccountView": lambda data: parse_player_account_view(data),
    "FounderStakeView": lambda data: parse_founder_stake_view(data),
    "AttentionScoreUpdate": lambda data: parse_attention_score_update(data),
    "RewardProjection": lambda data: parse_reward_projection(data),
    "RewardClaim": lambda data: parse_reward_claim(data),
}


SEASON1_PAYLOAD_VALIDATORS: dict[str, Any] = {
    "SeasonAccountView": lambda payload_or_obj: validate_season_account_view(payload_or_obj),
    "GameAccountView": lambda payload_or_obj: validate_game_account_view(payload_or_obj),
    "StakeAccountView": lambda payload_or_obj: validate_stake_account_view(payload_or_obj),
    "PlayerAccountView": lambda payload_or_obj: validate_player_account_view(payload_or_obj),
    "FounderStakeView": lambda payload_or_obj: validate_founder_stake_view(payload_or_obj),
    "AttentionScoreUpdate": lambda payload_or_obj: validate_attention_score_update(payload_or_obj),
    "RewardProjection": lambda payload_or_obj: validate_reward_projection(payload_or_obj),
    "RewardClaim": lambda payload_or_obj: validate_reward_claim(payload_or_obj),
}


def parse_season1_payload(payload_type: str, data: Mapping[str, Any]) -> Serializable:
    parser = SEASON1_PAYLOAD_PARSERS.get(payload_type)
    if parser is None:
        raise ValueError(f"Unknown Season 1 payload_type: {payload_type}")
    return parser(data)


def validate_season1_payload(
    payload_type: str,
    payload_or_obj: Serializable | Mapping[str, Any],
) -> tuple[bool, tuple[str, ...]]:
    validator = SEASON1_PAYLOAD_VALIDATORS.get(payload_type)
    if validator is None:
        return (False, (f"unknown_payload_type: {payload_type}",))
    return validator(payload_or_obj)


def parse_season_account_view(data: Mapping[str, Any]) -> SeasonAccountView:
    return SeasonAccountView.from_dict(_normalize_season_account_payload(data))


def validate_season_account_view(
    view_or_payload: SeasonAccountView | Mapping[str, Any],
) -> tuple[bool, tuple[str, ...]]:
    return _validate_account_view_common(
        view_or_payload,
        parse_season_account_view,
        min_fields=("season_id", "authority", "towel_mint", "started_at"),
    )


def parse_game_account_view(data: Mapping[str, Any]) -> GameAccountView:
    return GameAccountView.from_dict(_normalize_game_account_payload(data))


def validate_game_account_view(
    view_or_payload: GameAccountView | Mapping[str, Any],
) -> tuple[bool, tuple[str, ...]]:
    try:
        view = view_or_payload if isinstance(view_or_payload, GameAccountView) else parse_game_account_view(view_or_payload)
    except Exception as err:  # noqa: BLE001
        return (False, (f"parse_error: {err}",))

    errors: list[str] = []
    if view.season_id <= 0:
        errors.append("season_id must be > 0")
    if view.game_id <= 0:
        errors.append("game_id must be > 0")
    if view.attention_score_bps < 0 or view.attention_score_bps > 10_000:
        errors.append("attention_score_bps must be between 0 and 10000")

    deduped = tuple(dict.fromkeys(errors))
    return (not deduped, deduped)


def parse_stake_account_view(data: Mapping[str, Any]) -> StakeAccountView:
    return StakeAccountView.from_dict(_normalize_stake_account_payload(data))


def validate_stake_account_view(
    view_or_payload: StakeAccountView | Mapping[str, Any],
) -> tuple[bool, tuple[str, ...]]:
    try:
        view = view_or_payload if isinstance(view_or_payload, StakeAccountView) else parse_stake_account_view(view_or_payload)
    except Exception as err:  # noqa: BLE001
        return (False, (f"parse_error: {err}",))

    errors: list[str] = []
    if not view.owner:
        errors.append("owner must be non-empty")
    if view.season_id <= 0:
        errors.append("season_id must be > 0")
    if view.game_id <= 0:
        errors.append("game_id must be > 0")
    if view.amount < 0:
        errors.append("amount must be >= 0")

    deduped = tuple(dict.fromkeys(errors))
    return (not deduped, deduped)


def parse_player_account_view(data: Mapping[str, Any]) -> PlayerAccountView:
    return PlayerAccountView.from_dict(_normalize_player_account_payload(data))


def validate_player_account_view(
    view_or_payload: PlayerAccountView | Mapping[str, Any],
) -> tuple[bool, tuple[str, ...]]:
    try:
        view = view_or_payload if isinstance(view_or_payload, PlayerAccountView) else parse_player_account_view(view_or_payload)
    except Exception as err:  # noqa: BLE001
        return (False, (f"parse_error: {err}",))

    errors: list[str] = []
    if not view.owner:
        errors.append("owner must be non-empty")
    if view.season_id <= 0:
        errors.append("season_id must be > 0")
    if view.issued_towel_balance < 0:
        errors.append("issued_towel_balance must be >= 0")
    if view.staked_towel < 0:
        errors.append("staked_towel must be >= 0")
    if view.claimed_rewards < 0:
        errors.append("claimed_rewards must be >= 0")

    deduped = tuple(dict.fromkeys(errors))
    return (not deduped, deduped)


def parse_founder_stake_view(data: Mapping[str, Any]) -> FounderStakeView:
    return FounderStakeView.from_dict(_normalize_founder_stake_payload(data))


def validate_founder_stake_view(
    view_or_payload: FounderStakeView | Mapping[str, Any],
) -> tuple[bool, tuple[str, ...]]:
    try:
        view = view_or_payload if isinstance(view_or_payload, FounderStakeView) else parse_founder_stake_view(view_or_payload)
    except Exception as err:  # noqa: BLE001
        return (False, (f"parse_error: {err}",))

    errors: list[str] = []
    if not view.owner:
        errors.append("owner must be non-empty")
    if view.season_id <= 0:
        errors.append("season_id must be > 0")
    if view.amount < 0:
        errors.append("amount must be >= 0")

    deduped = tuple(dict.fromkeys(errors))
    return (not deduped, deduped)


def parse_attention_score_update(data: Mapping[str, Any]) -> AttentionScoreUpdate:
    return AttentionScoreUpdate.from_dict(_normalize_attention_score_payload(data))


def validate_attention_score_update(
    update_or_payload: AttentionScoreUpdate | Mapping[str, Any],
) -> tuple[bool, tuple[str, ...]]:
    try:
        update = (
            update_or_payload
            if isinstance(update_or_payload, AttentionScoreUpdate)
            else parse_attention_score_update(update_or_payload)
        )
    except Exception as err:  # noqa: BLE001
        return (False, (f"parse_error: {err}",))

    errors: list[str] = []
    if update.season_id <= 0:
        errors.append("season_id must be > 0")
    if update.game_id <= 0:
        errors.append("game_id must be > 0")
    if update.attention_score_bps < 0 or update.attention_score_bps > 10_000:
        errors.append("attention_score_bps must be between 0 and 10000")
    if update.updated_by is not None and not update.updated_by:
        errors.append("updated_by must be non-empty when provided")

    deduped = tuple(dict.fromkeys(errors))
    return (not deduped, deduped)


def parse_reward_projection(data: Mapping[str, Any]) -> RewardProjection:
    return RewardProjection.from_dict(_normalize_reward_projection_payload(data))


def validate_reward_projection(
    projection_or_payload: RewardProjection | Mapping[str, Any],
) -> tuple[bool, tuple[str, ...]]:
    try:
        projection = (
            projection_or_payload
            if isinstance(projection_or_payload, RewardProjection)
            else parse_reward_projection(projection_or_payload)
        )
    except Exception as err:  # noqa: BLE001
        return (False, (f"parse_error: {err}",))

    errors: list[str] = []
    if not projection.projection_id:
        errors.append("projection_id must be non-empty")
    if not projection.owner:
        errors.append("owner must be non-empty")
    if projection.season_id <= 0:
        errors.append("season_id must be > 0")
    if projection.staked_towel < 0:
        errors.append("staked_towel must be >= 0")
    if projection.total_staked < 0:
        errors.append("total_staked must be >= 0")
    if projection.reward_pool_total < 0:
        errors.append("reward_pool_total must be >= 0")
    if projection.reward_pool_remaining < 0:
        errors.append("reward_pool_remaining must be >= 0")
    if projection.projected_payout < 0:
        errors.append("projected_payout must be >= 0")
    if projection.reward_pool_remaining > projection.reward_pool_total:
        errors.append("reward_pool_remaining must be <= reward_pool_total")

    deduped = tuple(dict.fromkeys(errors))
    return (not deduped, deduped)


def parse_reward_claim(data: Mapping[str, Any]) -> RewardClaim:
    return RewardClaim.from_dict(_normalize_reward_claim_payload(data))


def validate_reward_claim(
    claim_or_payload: RewardClaim | Mapping[str, Any],
) -> tuple[bool, tuple[str, ...]]:
    try:
        claim = claim_or_payload if isinstance(claim_or_payload, RewardClaim) else parse_reward_claim(claim_or_payload)
    except Exception as err:  # noqa: BLE001
        return (False, (f"parse_error: {err}",))

    errors: list[str] = []
    if not claim.claim_id:
        errors.append("claim_id must be non-empty")
    if not claim.owner:
        errors.append("owner must be non-empty")
    if claim.season_id <= 0:
        errors.append("season_id must be > 0")
    if claim.amount < 0:
        errors.append("amount must be >= 0")
    if claim.status not in {"claimed", "rejected", "pending"}:
        errors.append("status must be one of: claimed,rejected,pending")

    deduped = tuple(dict.fromkeys(errors))
    return (not deduped, deduped)


def _normalize_base(data: Mapping[str, Any]) -> dict[str, Any]:
    normalized = dict(data)
    if "schema_version" not in normalized:
        normalized["schema_version"] = DEFAULT_SCHEMA_VERSION
    return normalized


def _normalize_season_account_payload(data: Mapping[str, Any]) -> dict[str, Any]:
    normalized = _normalize_base(data)

    _set_if_missing(normalized, "season_id", _first_of(normalized, "seasonId"))
    _set_if_missing(normalized, "authority", _first_of(normalized, "authority_pubkey", "authorityPubkey"))
    _set_if_missing(normalized, "towel_mint", _first_of(normalized, "towelMint"))

    started = _first_of(normalized, "start_ts", "startTs")
    if started is not None and "started_at" not in normalized:
        normalized["started_at"] = _epoch_to_iso8601(started)

    ended = _first_of(normalized, "end_ts", "endTs")
    if ended is not None and "ended_at" not in normalized:
        normalized["ended_at"] = _epoch_to_iso8601(ended)

    _set_if_missing(normalized, "reward_pool_total", _first_of(normalized, "rewardPoolTotal"))
    _set_if_missing(normalized, "reward_pool_remaining", _first_of(normalized, "rewardPoolRemaining"))
    _set_if_missing(normalized, "total_staked", _first_of(normalized, "totalStaked"))
    _set_if_missing(normalized, "founder_locked_total", _first_of(normalized, "founderLockedTotal"))
    return normalized


def _normalize_game_account_payload(data: Mapping[str, Any]) -> dict[str, Any]:
    normalized = _normalize_base(data)
    _set_if_missing(normalized, "season_id", _first_of(normalized, "seasonId"))
    _set_if_missing(normalized, "game_id", _first_of(normalized, "gameId"))
    _set_if_missing(normalized, "attention_score_bps", _first_of(normalized, "attentionScoreBps"))
    return normalized


def _normalize_stake_account_payload(data: Mapping[str, Any]) -> dict[str, Any]:
    normalized = _normalize_base(data)
    _set_if_missing(normalized, "season_id", _first_of(normalized, "seasonId"))
    _set_if_missing(normalized, "game_id", _first_of(normalized, "gameId"))
    return normalized


def _normalize_player_account_payload(data: Mapping[str, Any]) -> dict[str, Any]:
    normalized = _normalize_base(data)
    _set_if_missing(normalized, "season_id", _first_of(normalized, "seasonId"))
    _set_if_missing(normalized, "issued_towel_balance", _first_of(normalized, "issuedTowelBalance"))
    _set_if_missing(normalized, "staked_towel", _first_of(normalized, "stakedTowel"))
    _set_if_missing(normalized, "claimed_rewards", _first_of(normalized, "claimedRewards"))
    _set_if_missing(normalized, "has_claimed", _first_of(normalized, "hasClaimed"))
    return normalized


def _normalize_founder_stake_payload(data: Mapping[str, Any]) -> dict[str, Any]:
    normalized = _normalize_base(data)
    _set_if_missing(normalized, "season_id", _first_of(normalized, "seasonId"))
    return normalized


def _normalize_attention_score_payload(data: Mapping[str, Any]) -> dict[str, Any]:
    normalized = _normalize_game_account_payload(data)
    _set_if_missing(normalized, "updated_at", _first_of(normalized, "updatedAt", "scored_at", "scoredAt"))
    _set_if_missing(normalized, "updated_by", _first_of(normalized, "updatedBy", "authority"))
    return normalized


def _normalize_reward_projection_payload(data: Mapping[str, Any]) -> dict[str, Any]:
    normalized = _normalize_base(data)
    _set_if_missing(normalized, "projection_id", _first_of(normalized, "projectionId"))
    _set_if_missing(normalized, "season_id", _first_of(normalized, "seasonId"))
    _set_if_missing(normalized, "projected_at", _first_of(normalized, "projectedAt", "computed_at", "computedAt"))
    _set_if_missing(normalized, "staked_towel", _first_of(normalized, "stakedTowel", "staked_amount", "stakedAmount"))
    _set_if_missing(normalized, "total_staked", _first_of(normalized, "totalStaked"))
    _set_if_missing(normalized, "reward_pool_total", _first_of(normalized, "rewardPoolTotal"))
    _set_if_missing(normalized, "reward_pool_remaining", _first_of(normalized, "rewardPoolRemaining"))
    _set_if_missing(normalized, "projected_payout", _first_of(normalized, "projectedPayout"))
    return normalized


def _normalize_reward_claim_payload(data: Mapping[str, Any]) -> dict[str, Any]:
    normalized = _normalize_base(data)
    _set_if_missing(normalized, "claim_id", _first_of(normalized, "claimId"))
    _set_if_missing(normalized, "season_id", _first_of(normalized, "seasonId"))
    _set_if_missing(normalized, "claimed_at", _first_of(normalized, "claimedAt"))
    _set_if_missing(normalized, "transaction_signature", _first_of(normalized, "transactionSignature", "tx", "tx_sig"))
    return normalized


def _set_if_missing(target: dict[str, Any], key: str, value: Any) -> None:
    if key not in target and value is not None:
        target[key] = value


def _first_of(mapping: Mapping[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in mapping:
            return mapping[key]
    return None


def _epoch_to_iso8601(value: int | float | str) -> str:
    epoch = int(value)
    return datetime.fromtimestamp(epoch, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def _validate_account_view_common(
    view_or_payload: SeasonAccountView | Mapping[str, Any],
    parser: Any,
    min_fields: tuple[str, ...],
) -> tuple[bool, tuple[str, ...]]:
    try:
        view = view_or_payload if isinstance(view_or_payload, SeasonAccountView) else parser(view_or_payload)
    except Exception as err:  # noqa: BLE001
        return (False, (f"parse_error: {err}",))

    errors: list[str] = []
    if view.season_id <= 0:
        errors.append("season_id must be > 0")
    if not view.authority:
        errors.append("authority must be non-empty")
    if not view.towel_mint:
        errors.append("towel_mint must be non-empty")
    if view.reward_pool_total < 0:
        errors.append("reward_pool_total must be >= 0")
    if view.reward_pool_remaining < 0:
        errors.append("reward_pool_remaining must be >= 0")
    if view.total_staked < 0:
        errors.append("total_staked must be >= 0")
    if view.founder_locked_total < 0:
        errors.append("founder_locked_total must be >= 0")

    for field_name in min_fields:
        if getattr(view, field_name, None) in (None, ""):
            errors.append(f"{field_name} must be present")

    deduped = tuple(dict.fromkeys(errors))
    return (not deduped, deduped)
