# Release Guide

## 1) Create GitHub repo

Create `MetaSPN/metaspn-schemas` and connect this local repo:

```bash
git remote add origin git@github.com:MetaSPN/metaspn-schemas.git
```

## 2) First push

```bash
git add .
git commit -m "release: metaspn-schemas v0.5.0"
git branch -M main
git push -u origin main
```

## 3) Configure PyPI trusted publishing

In PyPI for project `metaspn-schemas`:

1. Create project if it does not exist.
2. Add a Trusted Publisher:
   - Owner: `MetaSPN`
   - Repository: `metaspn-schemas`
   - Workflow file: `.github/workflows/publish.yml`
   - Environment: leave empty (unless you later gate with a GitHub environment)

## 4) Validate package locally (optional but recommended)

```bash
python -m pip install -e .[dev]
pytest -q
python -m build
python -m twine check dist/*
```

## 5) Release from GitHub

1. Create and push tag:

```bash
git tag v0.5.0
git push origin v0.5.0
```

2. Create a GitHub Release for tag `v0.5.0`.
3. Publishing workflow runs automatically and uploads to PyPI.

## 6) Verify

- GitHub Actions `CI` and `Publish` workflows green
- PyPI page shows uploaded sdist + wheel
- Install check:

```bash
python -m pip install metaspn-schemas==0.5.0
```

## Version bump checklist

- Update `pyproject.toml` project `version`
- Add changelog entry in `CHANGELOG.md`
- Commit, tag (`vX.Y.Z`), and create GitHub release
