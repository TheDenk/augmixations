# -*- coding: utf-8 -*-
import pytest

from augmixations.utils import generate_rect_coordinates, generate_parameter, unpack_mm_params


@pytest.mark.parametrize('params',
                         [(500, 500, 0, 0, 500, 500, 100, 100, 300, 300),
                          (1000, 2000, 0, 0, 2000, 1000, 300, 300, 600, 600),
                             (500, 1000, 0, 0, 500, 500, None, None, None, None),
                             (500, 700, None, None, None, None, None, None, None, None),
                             (300, 300, None, None, None, None, 100, 100, 300, 300)])
def test_generate_rect_coordinates(params):
    img_h, img_w, min_x, min_y, max_x, max_y, min_h, min_w, max_h, max_w = params
    rect = generate_rect_coordinates(img_h, img_w, min_x, min_y, max_x, max_y, min_h, min_w, max_h, max_w)
    x1, y1, x2, y2 = rect

    assert x1 < x2 and y1 < y2
    assert x1 >= 0 and y1 >= 0
    assert x2 <= img_w and y2 <= img_h


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
