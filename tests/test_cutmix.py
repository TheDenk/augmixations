# -*- coding: utf-8 -*-
import numpy as np
import pytest


from augmixations.cutmix import (
    shift_fg_rect_and_boxes,
    correct_foreground_boxes,
    SmartCutmix,
)


@pytest.mark.parametrize('params',
                         [(np.array([0, 0, 200, 300]),
                           np.array([np.array([10, 10, 50, 50]),
                                     np.array([20, 10, 60, 40])]), 50, 100,
                             np.array([50, 100, 250, 400]),
                             np.array([np.array([60, 110, 100, 150]),
                                       np.array([70, 110, 110, 140])]))])
def test_shift_fg_rect_and_boxes(params):
    rect, boxes, shift_x, shift_y, result_rect, result_boxes = params
    new_rect, new_boxes = shift_fg_rect_and_boxes(rect, boxes, shift_x, shift_y)

    assert np.array_equal(result_rect, new_rect)
    assert np.array_equal(result_boxes, new_boxes)


@pytest.mark.parametrize('params', [
    # Кропаем боксы внутри прямоугольника
    (np.array([np.array([50, 50, 150, 150])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.9, 0.1, 0.1,
     np.array([np.array([100, 100, 150, 150])]), np.array(['1'], dtype=object)),

    (np.array([np.array([50, 150, 150, 250])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.9, 0.1, 0.1,
     np.array([np.array([100, 150, 150, 200])]), np.array(['1'], dtype=object)),

    (np.array([np.array([150, 150, 250, 250])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.9, 0.1, 0.1,
     np.array([np.array([150, 150, 200, 200])]), np.array(['1'], dtype=object)),

    (np.array([np.array([150, 50, 250, 150])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.9, 0.1, 0.1,
     np.array([np.array([150, 100, 200, 150])]), np.array(['1'], dtype=object)),

    # Удаляем боксы внутри прямоугольника по площади: max_overlap=0.5
    (np.array([np.array([50, 50, 150, 150])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.5, 0.1, 0.1,
     np.array([]), np.array([], dtype=object)),

    (np.array([np.array([50, 150, 150, 250])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.5, 0.1, 0.1,
     np.array([]), np.array([], dtype=object)),

    (np.array([np.array([150, 150, 250, 250])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.5, 0.1, 0.1,
     np.array([]), np.array([], dtype=object)),

    (np.array([np.array([150, 50, 250, 150])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.5, 0.1, 0.1,
     np.array([]), np.array([], dtype=object)),

    # Удаляем боксы вне области прямоугольника
    (np.array([np.array([50, 50, 75, 75])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.9, 0.1, 0.1,
     np.array([]), np.array([], dtype=object)),

    (np.array([np.array([50, 225, 75, 250])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.9, 0.1, 0.1,
     np.array([]), np.array([], dtype=object)),

    (np.array([np.array([225, 225, 250, 250])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.9, 0.1, 0.1,
     np.array([]), np.array([], dtype=object)),

    (np.array([np.array([225, 50, 250, 75])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.9, 0.1, 0.1,
     np.array([]), np.array([], dtype=object)),

])
def test_correct_foreground_boxes(params):
    fg_boxes, fg_labels, rect, max_area, min_h, min_w, real_boxes, real_labels = params
    boxes, labels = correct_foreground_boxes(
        fg_boxes, fg_labels, rect, max_area, min_h, min_w)
    assert np.array_equal(real_boxes, boxes)
    assert np.array_equal(real_labels, labels)


# Чисто проверим, что метод работает)))
@pytest.mark.parametrize('params', [
    (np.ones((1000, 2000, 3), dtype=np.uint8)*255,
     np.array([np.array([50, 50, 150, 150])]),
     np.array(['1'], dtype=np.str),
     np.ones((600, 800, 3), dtype=np.uint8)*255,
     np.array([np.array([100, 100, 200, 200])]),
     np.array(['2'], dtype=np.str),
     {'crop_x': (75, 76), 'crop_y': (75, 76), 'rect_h': (150, 151), 'rect_w': (150, 151),
      'insert_x': (100, 101), 'insert_y': (100, 101), }, None,
     np.array([np.array([50, 50, 150, 150]), np.array([125, 125, 225, 225])]),
     np.array(['1', '2'], dtype=np.str)
     ),
    # Игнорируем боксы по минимальной высоте
    (np.ones((1000, 2000, 3), dtype=np.uint8)*255,
     np.array([np.array([50, 50, 150, 150])]),
     np.array(['1'], dtype=np.str),
     np.ones((600, 800, 3), dtype=np.uint8)*255,
     np.array([np.array([100, 100, 200, 200])]),
     np.array(['2'], dtype=np.str),
     {'crop_x': (75, 76), 'crop_y': (175, 176), 'rect_h': (150, 151),
      'rect_w': (150, 151), 'insert_x': (100, 101), 'insert_y': (100, 101), },
     {
        'max_overlap_area_ratio': 0.99,
         'min_height_result_ratio': 0.7,
        'min_width_result_ratio': 0.25,
        'max_height_intersection': 0.9,
        'max_width_intersection': 0.3,
    },
        np.array([]),
        np.array([]),
        # Игнорируем боксы по минимальной ширине
    ),
    (np.ones((1000, 2000, 3), dtype=np.uint8)*255,
     np.array([np.array([50, 50, 150, 150])]),
     np.array(['1'], dtype=np.str),
     np.ones((600, 800, 3), dtype=np.uint8)*255,
     np.array([np.array([100, 100, 200, 200])]),
     np.array(['2'], dtype=np.str),
     {'crop_x': (175, 176), 'crop_y': (75, 76),
      'rect_h': (150, 151), 'rect_w': (150, 151),
      'insert_x': (100, 101), 'insert_y': (100, 101), },
     {
        'max_overlap_area_ratio': 0.99,
        'min_height_result_ratio': 0.25,
        'min_width_result_ratio': 0.7,
        'max_height_intersection': 0.3,
        'max_width_intersection': 0.9,
    },
        np.array([]),
        np.array([]),
    ),
])
def test_cutmix(params):
    bg_img, bg_boxes, bg_labels, fg_img, fg_boxes, fg_labels, \
        crop_rect_config, process_boxes_config, real_boxes, real_labels = params

    cutmix = SmartCutmix(crop_rect_config, process_boxes_config)
    img, boxes, labels = cutmix(
        bg_img,
        bg_boxes,
        bg_labels,

        fg_img,
        fg_boxes,
        fg_labels,)

    assert np.array_equal(real_boxes, boxes)
    assert np.array_equal(real_labels, labels)


# Проверка, что метод не падает, когда некоторые параметры отсутствуют
@pytest.mark.parametrize('params', [
    (np.ones((1000, 2000, 3), dtype=np.uint8)*255,
     np.array([np.array([50, 50, 150, 150])]),
     np.array(['1'], dtype=np.str),
     np.ones((600, 800, 3), dtype=np.uint8)*255,
     np.array([np.array([100, 100, 200, 200])]),
     np.array(['2'], dtype=np.str),
     {'crop_y': (75, 76),
      'rect_h': (150, 151),
      'insert_x': (100, 101), },
     {
        'max_overlap_area_ratio': 0.99,
        'min_width_result_ratio': 0.7,
        'max_height_intersection': 0.3,
    },)
])
def test_cutmix_no_params(params):
    bg_img, bg_boxes, bg_labels, fg_img, fg_boxes, fg_labels, \
        crop_rect_config, process_boxes_config, = params

    cutmix = SmartCutmix(crop_rect_config, process_boxes_config)
    img, boxes, labels = cutmix(
        bg_img,
        bg_boxes,
        bg_labels,

        fg_img,
        fg_boxes,
        fg_labels,)

    assert img.shape == bg_img.shape
