# -*- coding: utf-8 -*-
import numpy as np
import pytest

from augmixations.core import (
    generate_rect_coordinates,
    insert_image_in_background,
    check_middle_part_overlap_critical,
    correct_box_if_full_side_overlap,
    correct_box_if_some_alnge_overlap,
    correct_background_boxes,
)


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


@pytest.mark.parametrize('params',
                         [(np.ones((500, 500, 3), dtype=np.uint8)*255,
                           np.ones((300, 300, 3), dtype=np.uint8)*255,
                           100, 100, 0, 0, 500, 500),
                          (np.ones((500, 700, 3), dtype=np.uint8)*255,
                           np.ones((300, 200, 3), dtype=np.uint8)*255,
                           100, 100, None, None, None, None), ])
def test_insert_image_in_background(params):
    bg_img, fg_img, start_x, start_y, min_x, min_y, max_x, max_y = params

    out_img, (shift_x, shift_y) = insert_image_in_background(
        bg_img, fg_img, start_x, start_y, min_x, min_y, max_x, max_y)

    if max_x is not None:
        assert start_x + shift_x <= max_x
    if min_x is not None:
        assert start_x + shift_x >= min_x
    if max_y is not None:
        assert start_y + shift_y <= max_y
    if min_y is not None:
        assert start_y + shift_y >= min_y

    assert out_img.shape == bg_img.shape


@pytest.mark.parametrize('params', [
    ({'x1': 75, 'y1': 25, 'x2': 125, 'y2': 125, 'area': 50*100, 'height': 100, 'width': 50},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.3, 0.9, 0.9, np.array([50, 50, 150, 150]), True),
    ({'x1': 75, 'y1': 25, 'x2': 125, 'y2': 125, 'area': 50*100, 'height': 100, 'width': 50},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.4, 0.9, 0.9, np.array([50, 50, 150, 150]), False),
    ({'x1': 25, 'y1': 75, 'x2': 125, 'y2': 125,  'area': 50*100, 'height': 50, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.3, 0.9, 0.9, np.array([50, 50, 150, 150]), True),
    ({'x1': 25, 'y1': 75, 'x2': 125, 'y2': 125, 'area': 50*100, 'height': 50, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.4, 0.9, 0.9, np.array([50, 50, 150, 150]), False),
    ({'x1': 25, 'y1': 75, 'x2': 125, 'y2': 125, 'area': 50*100, 'height': 50, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.3, 0.9, 0.9, np.array([50, 50, 150, 150]), True),
    ({'x1': 75, 'y1': 75, 'x2': 125, 'y2': 175, 'area': 50*100, 'height': 100, 'width': 50},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.4, 0.9, 0.9, np.array([50, 50, 150, 150]), False),
    ({'x1': 75, 'y1': 75, 'x2': 125, 'y2': 175, 'area': 50*100, 'height': 100, 'width': 50},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.3, 0.9, 0.9, np.array([50, 50, 150, 150]), True),
    ({'x1': 75, 'y1': 75, 'x2': 175, 'y2': 125, 'area': 50*100, 'height': 50, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.4, 0.9, 0.9, np.array([50, 50, 150, 150]), False),
    ({'x1': 75, 'y1': 75, 'x2': 175, 'y2': 125, 'area': 50*100, 'height': 50, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.3, 0.9, 0.9, np.array([50, 50, 150, 150]), True),

    #  Вариант изменения бокса,
    #  если перекрыта большая часть одной из сторон
    ({'x1': 75, 'y1': 25, 'x2': 225, 'y2': 100, 'area': 75*150, 'height': 75, 'width': 150},
     {'x1': 50, 'y1': 50, 'x2': 250, 'y2': 250, 'area': 200*200, 'height': 200, 'width': 200},
     0.9, 0.9, 0.6, np.array([50, 100, 250, 250]), False),

    ({'x1': 75, 'y1': 200, 'x2': 225, 'y2': 300, 'area': 150*100, 'height': 100, 'width': 150},
     {'x1': 50, 'y1': 50, 'x2': 250, 'y2': 250, 'area': 200*200, 'height': 200, 'width': 200},
     0.9, 0.9, 0.6, np.array([50, 50, 250, 200]), False),

    ({'x1': 25, 'y1': 75, 'x2': 100, 'y2': 225, 'area': 75*150, 'height': 150, 'width': 75},
     {'x1': 50, 'y1': 50, 'x2': 250, 'y2': 250, 'area': 200*200, 'height': 200, 'width': 200},
     0.9, 0.6, 0.9, np.array([100, 50, 250, 250]), False),

    ({'x1': 200, 'y1': 75, 'x2': 300, 'y2': 225, 'area': 100*150, 'height': 150, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 250, 'y2': 250, 'area': 200*200, 'height': 200, 'width': 200},
     0.9, 0.6, 0.9, np.array([50, 50, 200, 250]), False),

    # Вставленная картинка в центре бокса, но очень большая
    ({'x1': 55, 'y1': 55, 'x2': 245, 'y2': 245, 'area': 190*190, 'height': 190, 'width': 190},
     {'x1': 50, 'y1': 50, 'x2': 250, 'y2': 250, 'area': 200*200, 'height': 200, 'width': 200},
     0.5, 0.9, 0.9, np.array([50, 50, 250, 250]), True),

    # Вставленная картинка с полным вертикальным перекрытием по центру
    ({'x1': 55, 'y1': 0, 'x2': 245, 'y2': 300, 'area': 190*300, 'height': 300, 'width': 190},
     {'x1': 50, 'y1': 50, 'x2': 250, 'y2': 250, 'area': 200*200, 'height': 200, 'width': 200},
     0.5, 0.9, 0.9, np.array([50, 50, 250, 250]), True),

    # Вставленная картинка с полным горизонтальным перекрытием по центру
    ({'x1': 0, 'y1': 55, 'x2': 300, 'y2': 245, 'area': 190*300, 'height': 190, 'width': 300},
     {'x1': 50, 'y1': 50, 'x2': 250, 'y2': 250, 'area': 200*200, 'height': 200, 'width': 200},
     0.5, 0.9, 0.9, np.array([50, 50, 250, 250]), True),

])
def test_check_middle_part_overlap_critical(params):
    rect_info, box_info, max_overlap_area_ratio, max_h_overlap, max_w_overlap, true_box, true_overlap = params
    new_box, critical_overlap = check_middle_part_overlap_critical(
        rect_info,
        box_info,
        max_overlap_area_ratio,
        max_h_overlap,
        max_w_overlap,
        debug=True,
        label='Test box',)
    assert critical_overlap == true_overlap
    assert np.array_equal(true_box, new_box)


@pytest.mark.parametrize('params', [
    # Перекрытие одной из сторон полностью
    # коэф. перекрываемой прощади для всех вариантов - 0.75
    ({'x1': 25, 'y1': 25, 'x2': 125, 'y2': 175, 'area': 100*150, 'height': 150, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.8, np.array([125, 50, 150, 150]), False),
    ({'x1': 25, 'y1': 25, 'x2': 125, 'y2': 175, 'area': 100*150, 'height': 150, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.7, np.array([125, 50, 150, 150]), True),

    ({'x1': 25, 'y1': 25, 'x2': 175, 'y2': 125, 'area': 150*100, 'height': 100, 'width': 150},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.8, np.array([50, 125, 150, 150]), False),
    ({'x1': 25, 'y1': 25, 'x2': 175, 'y2': 125, 'area': 150*100, 'height': 100, 'width': 150},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.7, np.array([50, 125, 150, 150]), True),

    ({'x1': 75, 'y1': 25, 'x2': 175, 'y2': 175, 'area': 150*100, 'height': 150, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.8, np.array([50, 50, 75, 150]), False),
    ({'x1': 75, 'y1': 25, 'x2': 175, 'y2': 175, 'area': 150*100, 'height': 150, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.7, np.array([50, 50, 75, 150]), True),

    ({'x1': 25, 'y1': 75, 'x2': 175, 'y2': 175, 'area': 150*100, 'height': 100, 'width': 150},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.8, np.array([50, 50, 150, 75]), False),
    ({'x1': 25, 'y1': 75, 'x2': 175, 'y2': 175, 'area': 150*100, 'height': 100, 'width': 150},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.7, np.array([50, 50, 150, 75]), True),
])
def test_correct_box_if_full_side_overlap(params):
    rect_info, box_info, max_overlap_area_ratio, true_box, real_overlap = params
    new_box, critical_overlap = correct_box_if_full_side_overlap(
        rect_info, box_info,
        max_overlap_area_ratio,
        debug=True,
        label='Test box',)
    assert real_overlap == critical_overlap
    assert np.array_equal(true_box, new_box)


@pytest.mark.parametrize('params', [
    # Тест перекрыт какой-либо из углов угол, проверка поочерёдно:
    # 1. Обычное перекрытие проходящее по всем порогам
    # 2. Уменьшение порога площади перекрытия, мин. коэф = 0.5625
    # 3. Увеличение порога минимальной ширины, мин. коэф = 0.25
    # 4. Увеличение порога минимальной высоты, мин. коэф = 0.25
    # 5. Увеличение погоров вин ширины и высоты и уменьшения порога мин площади

    # ЛЕВЫЙ ВЕРХНИЙ УГОЛ
    ({'x1': 25, 'y1': 25, 'x2': 125, 'y2': 125, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.9, 0.9, 0.7, np.array([50, 50, 150, 150]), False),

    ({'x1': 25, 'y1': 25, 'x2': 125, 'y2': 125, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.9, 0.9, 0.5, np.array([50, 50, 150, 150]), True),

    ({'x1': 25, 'y1': 25, 'x2': 125, 'y2': 125, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.7, 0.9, 0.7, np.array([125, 50, 150, 150]), False),

    ({'x1': 25, 'y1': 25, 'x2': 125, 'y2': 125, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.9, 0.7, 0.7, np.array([50, 125, 150, 150]), False),

    ({'x1': 25, 'y1': 25, 'x2': 125, 'y2': 125, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.7, 0.7, 0.5, np.array([125, 125, 150, 150]), True),

    # ПРАВЫЙ ВЕРХНИЙ УГОЛ
    ({'x1': 75, 'y1': 25, 'x2': 175, 'y2': 125, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.9, 0.9, 0.7, np.array([50, 50, 150, 150]), False),

    ({'x1': 75, 'y1': 25, 'x2': 175, 'y2': 125, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.9, 0.9, 0.5, np.array([50, 50, 150, 150]), True),

    ({'x1': 75, 'y1': 25, 'x2': 175, 'y2': 125, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.7, 0.9, 0.7, np.array([50, 50, 75, 150]), False),

    ({'x1': 75, 'y1': 25, 'x2': 175, 'y2': 125, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.9, 0.7, 0.7, np.array([50, 125, 150, 150]), False),

    ({'x1': 75, 'y1': 25, 'x2': 175, 'y2': 125, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.7, 0.7, 0.5, np.array([50, 125,  75, 150]), True),

    # ЛЕВЫЙ НИЖНИЙ УГОЛ
    ({'x1': 25, 'y1': 75, 'x2': 125, 'y2': 175, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.9, 0.9, 0.7, np.array([50, 50, 150, 150]), False),

    ({'x1': 25, 'y1': 75, 'x2': 125, 'y2': 175, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.9, 0.9, 0.5, np.array([50, 50, 150, 150]), True),

    ({'x1': 25, 'y1': 75, 'x2': 125, 'y2': 175, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.7, 0.9, 0.7, np.array([50, 125, 150, 150]), False),

    ({'x1': 25, 'y1': 75, 'x2': 125, 'y2': 175, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.9, 0.7, 0.7, np.array([50,  50, 150,  75]), False),

    ({'x1': 25, 'y1': 75, 'x2': 125, 'y2': 175, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.7, 0.7, 0.5, np.array([50, 125, 150, 75]), True),

    # ПРАВЫЙ НИЖНИЙ УГОЛ
    ({'x1': 100, 'y1': 100, 'x2': 200, 'y2': 200, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.9, 0.9, 0.5, np.array([50, 50, 150, 150]), False),

    ({'x1': 100, 'y1': 100, 'x2': 200, 'y2': 200, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.9, 0.9, 0.2, np.array([50, 50, 150, 150]), True),

    ({'x1': 100, 'y1': 100, 'x2': 200, 'y2': 200, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.4, 0.9, 0.7, np.array([50, 50, 100, 150]), False),

    ({'x1': 100, 'y1': 100, 'x2': 200, 'y2': 200, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.9, 0.4, 0.7, np.array([50,  50, 150,  100]), False),

    ({'x1': 100, 'y1': 100, 'x2': 200, 'y2': 200, 'area': 100*100, 'height': 100, 'width': 100},
     {'x1': 50, 'y1': 50, 'x2': 150, 'y2': 150, 'area': 100*100, 'height': 100, 'width': 100},
     0.4, 0.4, 0.2, np.array([50, 50, 100, 100]), True),
])
def test_correct_box_if_some_alnge_overlap(params):
    rect_info, box_info, max_h_overlap, max_w_overlap, max_overlap_area, true_box, real_overlap = params
    new_box, critical_overlap = correct_box_if_some_alnge_overlap(
        rect_info,
        box_info,
        max_h_overlap,
        max_w_overlap,
        max_overlap_area,
        debug=True,
        label='Test box',)
    assert real_overlap == critical_overlap
    assert np.array_equal(true_box, new_box)


@pytest.mark.parametrize('params', [
    # Нормальные прямоугольники с перекрытикем 0.25, проходящие по всем параметрам
    (np.array([np.array([50, 50, 150, 150])]), np.array([1], dtype=object),
     np.array([100, 100, 200, 200]), 0.5, 0.25, 0.25, 0.9, 0.9,
     np.array([np.array([50, 50, 150, 150])]), np.array([1.0], dtype=object)),

    (np.array([np.array([50, 150, 150, 250])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.5, 0.25, 0.25, 0.9, 0.9,
     np.array([np.array([50, 150, 150, 250])]), np.array(['1'], dtype=object)),

    (np.array([np.array([150, 150, 250, 250])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.5, 0.25, 0.25, 0.9, 0.9,
     np.array([np.array([150, 150, 250, 250])]), np.array(['1'], dtype=object)),

    (np.array([np.array([150, 50, 250, 150])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.5, 0.25, 0.25, 0.9, 0.9,
     np.array([np.array([150, 50, 250, 150])]), np.array(['1'], dtype=object)),

    # Изменяем коэф макс площади до 0.2
    (np.array([np.array([50, 50, 150, 150])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.2, 0.25, 0.25, 0.9, 0.9,
     np.array([]), np.array([])),

    (np.array([np.array([50, 150, 150, 250])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.2, 0.25, 0.25, 0.9, 0.9,
     np.array([]), np.array([])),

    (np.array([np.array([150, 150, 250, 250])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.2, 0.25, 0.25, 0.9, 0.9,
     np.array([]), np.array([])),

    (np.array([np.array([150, 50, 250, 150])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.2, 0.25, 0.25, 0.9, 0.9,
     np.array([]), np.array([])),

    # Изменяем коэф мин высоты до 0.7 (перекрытие 0.5) при ее изменении
    # с помощью уменьшения коэфта макс ширины до 0.2
    (np.array([np.array([50, 50, 150, 150])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.8, 0.7, 0.25, 0.9, 0.2,
     np.array([]), np.array([])),

    (np.array([np.array([50, 150, 150, 250])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.8, 0.7, 0.25, 0.9, 0.2,
     np.array([]), np.array([])),

    (np.array([np.array([150, 150, 250, 250])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.8, 0.7, 0.25, 0.9, 0.2,
     np.array([]), np.array([])),

    (np.array([np.array([150, 50, 250, 150])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.8, 0.7, 0.25, 0.9, 0.2,
     np.array([]), np.array([])),

    # Изменяем коэф мин ширины до 0.7 (перекрытие 0.5) при ее изменении
    # с помощью уменьшения коэфта макс ширины до 0.2
    (np.array([np.array([50, 50, 150, 150])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.8, 0.25, 0.7, 0.2, 0.9,
     np.array([]), np.array([])),

    (np.array([np.array([50, 150, 150, 250])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.8, 0.25, 0.7, 0.2, 0.9,
     np.array([]), np.array([])),

    (np.array([np.array([150, 150, 250, 250])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.8, 0.25, 0.7, 0.2, 0.9,
     np.array([]), np.array([])),

    (np.array([np.array([150, 50, 250, 150])]), np.array(['1'], dtype=object),
     np.array([100, 100, 200, 200]), 0.8, 0.25, 0.7, 0.2, 0.9,
     np.array([]), np.array([])),

    # Полное перекрытие бокса
    (np.array([np.array([50, 50, 150, 150])]), np.array(['1'], dtype=object),
     np.array([25, 25, 200, 200]), 0.8, 0.25, 0.25, 0.9, 0.9,
     np.array([]), np.array([])),

    # Перекрытие центральной части
    (np.array([np.array([50, 50, 150, 150])]), np.array(['1'], dtype=object),
     np.array([55, 55, 145, 145]), 0.5, 0.25, 0.25, 0.9, 0.9,
     np.array([]), np.array([])),

    # Перекрытие центральной части
    (np.array([np.array([50, 50, 150, 150])]), np.array(['1'], dtype=object),
     np.array([55, 55, 145, 145]), 0.5, 0.25, 0.25, 0.9, 0.9,
     np.array([]), np.array([])),

    # Критическое перекрытие верхней части бокса
    (np.array([np.array([50, 50, 150, 150])]), np.array(['1'], dtype=object),
     np.array([25, 25, 175, 120]), 0.5, 0.25, 0.25, 0.9, 0.9,
     np.array([]), np.array([])),
])
def test_correct_background_boxes(params):
    bg_boxes, bg_labels, image_rect, max_overlap, min_h, min_w, \
        max_h_overlap, max_w_overlap, real_boxes, real_labels = params
    boxes, labels = correct_background_boxes(
        bg_boxes, bg_labels, image_rect,
        max_overlap, min_h, min_w,
        max_h_overlap, max_w_overlap,
        debug=True)
    assert np.array_equal(real_boxes, boxes)
    assert np.array_equal(real_labels, labels)
