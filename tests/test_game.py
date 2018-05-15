"""
"""

import pytest
from hypothesis import given
from hypothesis.strategies import integers

from ludology import Game
from ludology.game import Outcome
from ludology.tools import canonicalize


zero = Game(0)
half = Game(1/2)
one = Game(1)
none = Game(-1)
star = Game({zero}, {zero})
star2 = Game({zero, star}, {zero, star})
up = Game({zero}, {star})
down = -up
pm = Game({1}, {-1})


@pytest.mark.parametrize(['g1', 'g2'], [
    (one, zero),
    (one, half),
    (one, none),
    (zero, none),
    (zero, -half),
    (up, zero),
    (half, up),
    (up + up, star),
    (zero, zero),
    (up, up),
])
def test_ge(g1, g2):
    """
    """
    assert g1 >= g2


@pytest.mark.parametrize(['g1', 'g2'], [
    (one, zero),
    (one, half),
    (one, none),
    (zero, none),
    (zero, -half),
    (up, zero),
    (half, up),
    (up + up, star),
])
def test_gt(g1, g2):
    """
    """
    assert g1 > g2


@pytest.mark.parametrize(['g1', 'g2'], [
    (zero, one),
    (half, one),
    (none, one),
    (none, zero),
    (-half, zero),
    (zero, up),
    (up, half),
    (star, up + up),
    (zero, zero),
    (up, up),
])
def test_le(g1, g2):
    """
    """
    assert g1 <= g2


@pytest.mark.parametrize(['g1', 'g2'], [
    (zero, one),
    (half, one),
    (none, one),
    (none, zero),
    (-half, zero),
    (zero, up),
    (up, half),
    (star, up + up),
])
def test_lt(g1, g2):
    """
    """
    assert g1 < g2


@pytest.mark.parametrize(['g1', 'g2'], [
    (star, zero),
    (star, up),
    (one, pm),
    (pm, none),
    (pm, star),
    (pm, zero),
])
def test_fuzzy_1(g1, g2):
    """
    """
    assert g1 | g2


def test_fuzzy_2():
    """
    """
    assert star | 0
    assert 0 | star


def test_equiv_1():
    """
    """
    g = Game({star})
    assert g == zero


def test_equiv_2():
    """
    """
    g = Game(right={star})
    assert g == zero


@pytest.mark.parametrize('g', [
    zero,
    star,
    star2,
])
def test_impartial(g):
    """
    """
    assert g.is_impartial


@pytest.mark.parametrize('g', [
    one,
    half,
    up,
    up + star,
    pm,
])
def test_not_impartial(g):
    """
    """
    assert not g.is_impartial


@pytest.mark.parametrize('g', [
    pm,
    Game({2}, {1}),
])
def test_switch(g):
    """
    """
    assert g.is_switch


@pytest.mark.parametrize('g', [
    zero,
    one,
    up,
    star,
])
def test_not_switch(g):
    """
    """
    assert not g.is_switch


@pytest.mark.parametrize(['g', 'bday'], [
    (zero, 0),
    (one, 1),
    (none, 1),
    (star, 1),
    (up, 2),
    (canonicalize(up + star), 2),
    (half, 2),
])
def test_birthday(g, bday):
    """
    """
    assert g.birthday == bday


@pytest.mark.parametrize(['a', 'b', 'c'], [
    (zero, zero, zero),
    (star, star, zero),
    (one, none, zero),
    (one, zero, one),
    (zero, one, one),
    (one, 0, one),
    (0, one, one),
    (one, star, Game({one}, {one})),
    (star, one, Game({one}, {one})),
])
def test_add(a, b, c):
    assert a + b == c


@pytest.mark.parametrize(['a', 'b', 'c'], [
    (zero, zero, zero),
    (star, star, star),
    (one, none, -1),
    (one + 1, 1, 2),
    (2, one, one + one),
])
def test_mul(a, b, c):
    assert a * b == c


@pytest.mark.parametrize(['g', 'o'], [
    (zero, Outcome.PREVIOUS),
    (star, Outcome.NEXT),
    (one, Outcome.LEFT),
    (up, Outcome.LEFT),
    (-up, Outcome.RIGHT),
])
def test_outcome(g, o):
    assert g.outcome == o


@pytest.mark.parametrize(['g', 'v'], [
    (star, '∗'),
    (pm, '±1'),
    (Game({Game(3)}, {Game(1)}), '2±1'),
    (up, '↑'),
    (2 * up, '2·↑'),
    (up + star, '↑∗'),
    (up + up + star, '2·↑∗'),
    (down, '↓'),
    (2 * down, '2·↓'),
    (down + star, '↓∗'),
    (down + down + star, '2·↓∗'),
    (Game({one}, {1}), '1∗'),
    (Game({0}, {Game({0}, {-2})}), '➕_2'),
    (Game({Game({2}, {0})}, {0}), '➖_2'),
    (star2, '∗2'),
    (Game({5/2, Game({4}, {2})}, {Game({-1}, {-2}), Game({0}, {-4})}), '{3±1,5/2|-2±2,-3/2±1/2}'),
    (Game({0}, {star2}), '{0|∗2}'),
    (Game({star2}, {0}), '{∗2|0}'),
])
def test_value(g, v):
    assert g.value == v


@given(integers(min_value=-7, max_value=7), integers(min_value=0, max_value=3))
def test_value_dyadic_rational(m, j):
    """
    """
    f = m/2**j
    n, d = f.as_integer_ratio()
    g = Game(f)
    assert g.value == (f"{n}/{d}" if d > 1 else f"{n}")
