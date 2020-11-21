# -*- coding: utf-8 -*-
import numpy as np
import pytest


@pytest.mark.parametrize('params', [(10, 10, 50, 100, 0.5, 10, 323), ])
def test_generate_points(params, hand_written_blot):
    mask_x, mask_y, mask_w, mask_h, intensivity, incline, p_count = params

    p = hand_written_blot.generate_points(mask_x, mask_y, mask_w, mask_h, intensivity, incline)

    assert isinstance(p, list)
    assert len(p) == 2


@pytest.mark.parametrize('params', [(np.ones((100, 100, 3), dtype=np.uint8),
                                     [[10, 20, 30, 40, 50], [10, 40, 50, 30, 40]]), ])
def test_draw_bezier_curve(params, hand_written_blot):
    img, points = params
    p = hand_written_blot.draw_bezier_curve(img, points)

    assert type(img) == type(p)
