# metaspn-schemas

Canonical, stdlib-only schema package for MetaSPN-compatible systems.

## Install

```bash
pip install metaspn-schemas
```

## Development

```bash
python -m pip install -e .[dev]
pytest -q
python -m build
python -m twine check dist/*
```

## Design constraints

- Tiny and dependency-light (stdlib only)
- Frozen dataclasses for immutable-by-default objects
- Explicit `schema_version` on all public objects
- `to_dict()` / `from_dict()` on every schema
- UTC ISO-8601 datetime serialization
- Traceability metadata (`trace_id`, `caused_by`, provenance)
- Privacy mode support (`to_dict(privacy_mode=True)` omits raw blobs)

## Example

```python
from datetime import timezone, datetime

from metaspn_schemas import SignalEnvelope
from metaspn_schemas.utils.ids import generate_id

signal = SignalEnvelope(
    signal_id=generate_id("signal"),
    timestamp=datetime.now(timezone.utc),
    source="linkedin.webhook",
    payload_type="SocialPostSeen",
    payload={"post_id": "123", "platform": "linkedin"},
    schema_version="0.1",
)

as_dict = signal.to_dict()
round_trip = SignalEnvelope.from_dict(as_dict)
```

## Public imports

```python
from metaspn_schemas import (
    SignalEnvelope,
    EmissionEnvelope,
    Task,
    Result,
    SocialPostSeen,
    ProfileEnriched,
    ScoresComputed,
)
```

## Package layout

```text
metaspn-schemas/
  pyproject.toml
  README.md
  src/metaspn_schemas/
    __init__.py
    core.py
    tasks.py
    entities.py
    social.py
    outcomes.py
    features.py
    state_fragments.py
    utils/
      ids.py
      time.py
      serde.py
  test/
    test_serde.py
    test_ids.py
    test_backcompat.py
```

## Release

Release automation is configured in:

- `.github/workflows/ci.yml`
- `.github/workflows/publish.yml`

See `RELEASE.md` for the end-to-end push + PyPI release flow.
