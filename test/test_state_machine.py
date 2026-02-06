from __future__ import annotations

from datetime import datetime, timezone

from metaspn_schemas.state_machine import (
    StateMachineConfig,
    StateTransitionRule,
    parse_state_machine_config,
    validate_state_machine_config,
)

NOW = datetime(2026, 2, 6, 0, 0, tzinfo=timezone.utc)


def test_parse_state_machine_config_current_shape() -> None:
    payload = {
        "config_id": "cfg_1",
        "machine_type": "default",
        "initial_state": "seen",
        "states": ["seen", "queued", "sent"],
        "terminal_states": ["sent"],
        "transitions": [
            {"from_state": "seen", "to_state": "queued", "event": "route"},
            {"from_state": "queued", "to_state": "sent", "event": "dispatch"},
        ],
    }

    config = parse_state_machine_config(payload)
    assert isinstance(config, StateMachineConfig)
    assert config.states == ("queued", "seen", "sent")


def test_validate_state_machine_config_success() -> None:
    config = StateMachineConfig(
        config_id="cfg_1",
        machine_type="default",
        initial_state="seen",
        states=("seen", "queued", "sent"),
        terminal_states=("sent",),
        transitions=(
            StateTransitionRule("seen", "queued", "route"),
            StateTransitionRule("queued", "sent", "dispatch"),
        ),
    )

    ok, errors = validate_state_machine_config(config)
    assert ok is True
    assert errors == ()


def test_validate_state_machine_config_failure() -> None:
    bad_payload = {
        "config_id": "cfg_bad",
        "machine_type": "default",
        "initial_state": "missing",
        "states": ["seen"],
        "transitions": [{"from_state": "seen", "to_state": "done", "event": "route"}],
    }

    ok, errors = validate_state_machine_config(bad_payload)
    assert ok is False
    assert "initial_state must exist in states" in errors
    assert "transition to_state not in states: done" in errors
