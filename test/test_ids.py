from __future__ import annotations

from metaspn_schemas.utils.ids import generate_id


def test_generate_id_default() -> None:
    value = generate_id()
    assert "_" not in value
    assert len(value) == 32


def test_generate_id_with_known_prefix() -> None:
    value = generate_id("signal")
    assert value.startswith("s_")
    assert len(value.split("_", 1)[1]) == 32


def test_generate_id_with_custom_prefix() -> None:
    value = generate_id("custom")
    assert value.startswith("custom_")
