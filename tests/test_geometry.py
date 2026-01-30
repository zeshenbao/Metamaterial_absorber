import pytest

from metamaterial_absorber import Absorber, Pattern, Tile, Wall

pytest.importorskip("cadquery")


@pytest.mark.cadquery
def test_absorber_build_creates_solids():
    wall = Wall(cross_section="block", tile_len=1.0, tile_wid=1.0, tile_height=1.0, export=False)
    pattern = Pattern()
    pattern.create_ver_rows_blueprint(pattern_len=2, pattern_wid=1, scale=1.0)

    absorber = Absorber(wall, pattern)
    absorber.build()

    solids = absorber.result.solids().vals()
    assert len(solids) > 0


@pytest.mark.cadquery
def test_absorber_export_custom_filename(tmp_path):
    wall = Wall(cross_section="triangle", export=False)
    pattern = Pattern()
    pattern.create_dots_blueprint(pattern_len=1, pattern_wid=1, scale=1.0)

    absorber = Absorber(wall, pattern)
    absorber.build()

    output = tmp_path / "custom_export.stl"
    exported = absorber.export(str(output))

    assert exported == str(output)
    assert output.exists()
    assert output.stat().st_size > 0


@pytest.mark.cadquery
def test_absorber_export_default_filename(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    wall = Wall(cross_section="dogleg", export=False)
    pattern = Pattern()
    pattern.create_hilbert_blueprint(iterations=1, scale=1.0)

    absorber = Absorber(wall, pattern)
    absorber.build()

    filename = absorber.export()
    expected = tmp_path / filename

    assert filename == "dogleg_hilbert_iter1.stl"
    assert expected.exists()


@pytest.mark.cadquery
def test_absorber_build_rejects_unknown_group():
    wall = Wall(cross_section="block", export=False)
    pattern = Pattern()
    pattern.blueprint = [Tile("unknown", "ver", [0, 0, 0])]
    pattern.name = "custom"

    absorber = Absorber(wall, pattern)

    with pytest.raises(ValueError, match="Unknown tile group"):
        absorber.build()
