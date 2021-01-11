# -*- coding: utf-8 -*-
import numpy as np
import pytest

from augmixations.cutout import SmartCutout

# Проверка, что метод не падает


@pytest.mark.parametrize('params', [
    (np.ones((500, 500, 3), dtype=np.uint8)*255,
     np.array([np.array([50, 50, 150, 150])]),
     np.array(['1'], dtype=np.str),
     {
        'crop_x': (None, None),
        'crop_y': (None, None),
        'rect_h': (100, None),
        'rect_w': (100, None),
        'transparency': (0.0, 0.05),
        'hole_nums': (0, 3),
    },
        {
        'max_overlap_area_ratio': 0.75,
        'min_height_result_ratio': 0.25,
        'min_width_result_ratio': 0.25,
        'max_height_intersection': 0.9,
        'max_width_intersection': 0.9,
    },)
])
def test_cutout(params):
    img, boxes, labels, cr_config, pb_config = params

    cutout = SmartCutout(cr_config, pb_config)
    n_img, n_boxes, n_labels = cutout(img, boxes, labels)

    assert n_img.shape == img.shape
