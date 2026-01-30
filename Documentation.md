# Documentation

This document describes the refactored `metamaterial_absorber` package (v0.1.x). For historical lab notes and early prototyping logs, see `History_log.md`.

## Installation

Recommended (conda + conda-forge):

```
conda create -n memab python=3.11
conda activate memab
conda install -c conda-forge cadquery
python -m pip install -e .
```

Pip-only (may require system dependencies):

```
python -m pip install -e ".[cadquery]"
```

## Usage

### CLI

```
metamaterial-absorber --pattern dots --cross-section triangle --pattern-len 5 --pattern-wid 5
```

You can also invoke the module directly:

```
python -m metamaterial_absorber --pattern dots --cross-section triangle --pattern-len 5 --pattern-wid 5
```

Common flags:
- `--pattern`: `ver_rows`, `dots`, `hilbert`
- `--cross-section`: `dogleg`, `triangle`, `block`
- `--pattern-len`, `--pattern-wid`, `--iterations`, `--scale`
- `--output`: custom STL filename
- `--export-wall-parts`: export individual wall components

### Python API

```python
from metamaterial_absorber import Absorber, Pattern, Wall

wall = Wall(cross_section="dogleg", tile_height=3.0, export=False)
pattern = Pattern()
pattern.create_ver_rows_blueprint(pattern_len=8, pattern_wid=4, scale=1.0)

absorber = Absorber(wall, pattern)
absorber.build()
absorber.export("dogleg_rows.stl")
```

## Core concepts

- **Wall**: Builds wall segments from a chosen cross section. Exports parts optionally.
- **Pattern**: Generates a blueprint (list of tiles + coordinates).
- **Tile**: Lightweight record representing group/type/coordinate.
- **Absorber**: Assembles tiles into a CadQuery workplane and exports STL.

## API reference (high level)

### `Absorber`
- `__init__(wall, pattern)`
- `build()`
- `export(filename: str | None = None) -> str`

### `Wall`
- `__init__(cross_section="dogleg", tile_len=1.0, tile_wid=1.0, tile_height=2.0, foundation_thickness=4.0, scale=1.0, export=True)`
- `set_cross_section(choice: str | None = None)`
- `export_parts()`

### `Pattern`
- `create_hilbert_blueprint(iterations=2, scale=1.0)`
- `create_ver_rows_blueprint(pattern_len=5.0, pattern_wid=5.0, scale=1.0)`
- `create_dots_blueprint(pattern_len=10.0, pattern_wid=10.0, scale=1.0)`

### `Tile`
- `goto(coord)`
- `translate(delta)`
- `as_tuple()`

## Testing

```
python -m pip install -e ".[dev]"
python -m pytest -q
```

CadQuery geometry tests (requires CadQuery):

```
python -m pytest -q -m cadquery
```

## CI/CD

GitHub Actions runs two jobs:
- `test`: lint, format check, pytest, and build across Python 3.10–3.12.
- `cadquery`: geometry tests in a conda-forge environment.

## Project structure

- `src/metamaterial_absorber/`: package code
- `tests/`: unit tests
- `examples/`: runnable examples
- `README.md`: quick overview

## Troubleshooting

- **ImportError: cadquery is required**
  Install CadQuery via conda-forge (recommended) or `pip install -e ".[cadquery]"`.
- **No STL output**
  Ensure you call `Absorber.build()` before `Absorber.export()`.
