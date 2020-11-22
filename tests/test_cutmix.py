# -*- coding: utf-8 -*-
import numpy as np
import pytest

from augmixations.cutmix import insert_image_in_background, \
    shift_fg_rect_and_boxes, check_middle_part_overlap_critical, \
    correct_box_if_full_side_overlap, correct_box_if_some_alnge_overlap, \
    correct_background_boxes, correct_foreground_boxes, Cutmix


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

    cutmix = Cutmix(crop_rect_config, process_boxes_config)
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

    cutmix = Cutmix(crop_rect_config, process_boxes_config)
    img, boxes, labels = cutmix(
        bg_img,
        bg_boxes,
        bg_labels,

        fg_img,
        fg_boxes,
        fg_labels,)

    assert img.shape == bg_img.shape
