# -*- coding: utf-8 -*-
import pytest

from augmixations.utils import generate_parameter, unpack_mm_params


@pytest.mark.parametrize('params', [(1, 5), (0.1, 1.0), (5, 5)])
def test_generate_parameter(params):
    p1, p2 = params
    p = generate_parameter(p1, p2)

    assert p <= p2 and p >= p1


@pytest.mark.parametrize('params', [(1.0, 5), (1, 'Hello'), (None, 5)])
def test_generate_parameter_raise(params):
    p1, p2 = params
    with pytest.raises(Exception):
        _ = generate_parameter(p1, p2)


@pytest.mark.parametrize('params', [([1, 2], (1, 2)),
                                    ((2, 3), (2, 3)),
                                    (1, (1, 1)),
                                    (0.0, (0.0, 0.0))])
def test_unpack_mm_params(params):
    p, answer = params
    a = unpack_mm_params(p)

    assert answer == a


@pytest.mark.parametrize('params', [('Hello', None), (None, None)])
def test_unpack_mm_params_raise(params):
    p, answer = params
    with pytest.raises(Exception):
        _ = unpack_mm_params(p)
