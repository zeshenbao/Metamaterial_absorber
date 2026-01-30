from metamaterial_absorber.patterns import Pattern


def test_hilbert_system_iteration_1():
    assert Pattern._gen_hilbert_system(1) == "+--+"


def test_hilbert_blueprint_length_and_groups():
    pattern = Pattern()
    pattern.create_hilbert_blueprint(iterations=1, scale=1.0)
    assert len(pattern.blueprint) == 4
    assert all(tile.group == "corners" for tile in pattern.blueprint)


def test_ver_rows_blueprint_size():
    pattern = Pattern()
    pattern.create_ver_rows_blueprint(pattern_len=2, pattern_wid=3, scale=1.0)
    assert len(pattern.blueprint) == 6
    assert pattern.blueprint[0].coord == [0.0, 0.0, 0.0]
    assert pattern.blueprint[-1].coord == [1.0, 2.0, 0.0]


def test_dots_blueprint_size():
    pattern = Pattern()
    pattern.create_dots_blueprint(pattern_len=2, pattern_wid=3, scale=2.0)
    assert len(pattern.blueprint) == 6
    assert pattern.blueprint[0].coord == [0.0, 0.0, 0.0]
    assert pattern.blueprint[-1].coord == [2.0, 4.0, 0.0]
