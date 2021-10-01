# -*- coding: utf-8 -*-
import numpy as np
import pytest

from augmixations.mixin import Mixin


@pytest.mark.parametrize('params', [
    (np.ones((1000, 2000, 3), dtype=np.uint8)*255,
     np.array([np.array([50, 50, 150, 150])]),
     np.array(['1'], dtype=str),
     np.ones((1000, 2000, 3), dtype=np.uint8)*255,
     np.array([np.array([200, 200, 500, 500])]),
     np.array(['2'], dtype=str),
     np.array([np.array([50, 50, 150, 150]), np.array([200, 200, 500, 500])]),
     np.array(['1', '2'], dtype=str)
     ),
    (np.ones((1000, 2000, 3), dtype=np.uint8)*255,
     np.array([np.array([50, 50, 150, 150])]),
     np.array(['1'], dtype=str),
     np.ones((1000, 2000, 3), dtype=np.uint8)*255,
     np.array([np.array([200, 200, 500, 500])]),
     np.array(['2'], dtype=str),
     np.array([np.array([50, 50, 150, 150]), np.array([200, 200, 500, 500])]),
     np.array(['1', '2'], dtype=str),
     ),
    (np.ones((1000, 2000, 3), dtype=np.uint8)*255,
     np.array([np.array([50, 50, 150, 150])]),
     np.array(['2'], dtype=str),
     np.ones((1000, 2000, 3), dtype=np.uint8)*255,
     np.array([np.array([500, 500, 700, 700])]),
     np.array(['1'], dtype=str),
     np.array([np.array([50, 50, 150, 150]), np.array([500, 500, 700, 700])]),
     np.array(['2', '1'], dtype=str),
     ),
])
def test_cutmix(params):
    bg_img, bg_boxes, bg_labels, fg_img, fg_boxes, fg_labels, \
        real_boxes, real_labels = params

    cutmix = Mixin()
    img, boxes, labels = cutmix(
        bg_img,
        bg_boxes,
        bg_labels,

        fg_img,
        fg_boxes,
        fg_labels,)

    assert np.array_equal(real_boxes, boxes)
    assert np.array_equal(real_labels, labels)
    assert bg_img.shape == img.shape
    assert fg_img.shape == img.shape
