# -*- coding: utf-8 -*-
import numpy as np

from .utils import unpack_mm_params
from .core import (
    generate_rect_coordinates,
    insert_image_in_background,
    correct_background_boxes,
)
from .configs import (
    cutmix_crop_rect_config,
    cutmix_process_box_config
)


def shift_fg_rect_and_boxes(rect: np.array, boxes: np.array, shift_x: int, shift_y: int):
    """
    Description:
    The shift of the boxes is necessary after the cut image is inserted into
    a new random place on the background.
    Due to the fact that the starting and inserted places do not match,
    it is necessary to shift the boxes.

    Parameters:
    rect (np.array) - image rect coordinates
    boxes (np.array) - set of box coordinates
    shift_x (int) - X-axis shift
    shift_y (int) - Y-axis shift

    Returns:
    (new_rect, new_boxes) (np.array, np.array) - tuple of new image rectangle
        and box coordinates
    """
    x1, y1, x2, y2 = rect

    new_rect = np.array([
        x1 + shift_x,
        y1 + shift_y,
        x2 + shift_x,
        y2 + shift_y,
    ])

    new_boxes = boxes.copy()
    new_boxes[:, 0] += shift_x
    new_boxes[:, 1] += shift_y
    new_boxes[:, 2] += shift_x
    new_boxes[:, 3] += shift_y

    return new_rect, new_boxes


def correct_foreground_boxes(fg_boxes: np.array,
                             fg_labels: np.array,
                             image_rect: np.array,
                             max_overlap_area_ratio: np.array,
                             min_height_ratio: np.array,
                             min_width_ratio: np.array):
    """
    Description:
    Foreground boxes correction by custom parameters.

    Parameters:
    fg_boxes (np.array) - foreground boxes coordinates
    fg_labels (np.array) - foreground labels of boxes
    image_rect (np.array) - coordinates of rectangle that will be cutted from foreground
    max_overlap_area_ratio (float) - maximum box overlap threshold.
        If overlap is larger - box will be dropped
    min_height_ratio (float) - min part of height that should be exists or box will be dropped
    min_width_ratio (float) - min part of width that should be exists or box will be dropped

    Return:
    (new_box, critical_overlap_flag) - correct box coordinates and Boolean flag means
        that overlap exists and critical
    """
    x1, y1, x2, y2 = image_rect
    new_boxes = []
    new_labels = []

    # Поправляем боксы= вставленной картинки
    for i, (box, label) in enumerate(zip(fg_boxes, fg_labels)):
        f_x1, f_y1, f_x2, f_y2 = box
        start_box_height = f_y2 - f_y1
        start_box_width = f_x2 - f_x1

        l_side_in_rect = (f_x1 >= x1 and f_x1 <= x2)
        r_side_in_rect = (f_x2 >= x1 and f_x2 <= x2)
        t_side_in_rect = (f_y1 >= y1 and f_y1 <= y2)
        b_side_in_rect = (f_y2 >= y1 and f_y2 <= y2)

        # если какая-то часть бокса входит в новый прямоугольник
        if l_side_in_rect or r_side_in_rect or t_side_in_rect or b_side_in_rect:
            start_area = (f_x2 - f_x1) * (f_y2 - f_y1)
            # обрезаем части, которые вылезли за границу
            new_box = np.array([max(f_x1, x1), max(f_y1, y1), min(f_x2, x2), min(f_y2, y2)])

            end_box_height = new_box[3] - new_box[1]
            end_box_width = new_box[2] - new_box[0]
            end_box_area = end_box_height * end_box_width

            overlap_part = (start_area - end_box_area) / start_area

            if (end_box_height / start_box_height) < min_height_ratio:
                continue
            if (end_box_width / start_box_width) < min_width_ratio:
                continue
            if overlap_part > max_overlap_area_ratio:
                continue

            new_boxes.append(new_box)
            new_labels.append(label)
    return new_boxes, new_labels


class SmartCutmix:
    """
    Description:
    CutMix class. This class allows crop part of image from second image and paste it into first image.
    It also changes first and second boxes and labels.

    Init Parameters:

    crop_rect_config (dict) - Config with parameters of cut and insert coordinates
    process_boxes_config (dict) - Config with parameters of maximum box area overlap and maximum box side overlap
    """

    def __init__(self, crop_rect_config: dict = None,
                 process_boxes_config: dict = None,):
        self.cr_conf = cutmix_crop_rect_config if crop_rect_config is None else crop_rect_config
        self.pb_conf = cutmix_process_box_config if process_boxes_config is None else process_boxes_config

        for def_key, def_val in cutmix_crop_rect_config.items():
            if def_key not in self.cr_conf.keys() or self.cr_conf[def_key] is None:
                self.cr_conf[def_key] = def_val

        for def_key, def_val in cutmix_process_box_config.items():
            if def_key not in self.pb_conf.keys() or self.pb_conf[def_key] is None:
                self.pb_conf[def_key] = def_val

    def apply(self,
              bg_img: np.array,
              bg_boxes: np.array,
              bg_labels: np.array,

              fg_img: np.array,
              fg_boxes: np.array,
              fg_labels: np.array):
        """
        Description:
        Cutmix function. It function crop part of image from second image and paste it into first image.
        Function also changes first and second boxes and labels.

        Parameters:

        bg_img (np.array) - Background image. The image into which another image will be inserted.
        bg_boxes (np.array) - Boxes for background image.
        bg_labels (np.array) - Labels for background image.

        fg_img (np.array) - The image from which the rectangle will be cut
        fg_boxes (np.array) - Boxes for foreground image.
        fg_labels (np.array) - Labels for foreground image.

        Return:
        (new_image, new_boxes, new_labels) - New image, boxes and labels
        """
        crop_min_x, crop_max_x = unpack_mm_params(self.cr_conf['crop_x'])
        crop_min_y, crop_max_y = unpack_mm_params(self.cr_conf['crop_y'])
        rect_min_h, rect_max_h = unpack_mm_params(self.cr_conf['rect_h'])
        rect_min_w, rect_max_w = unpack_mm_params(self.cr_conf['rect_w'])

        insert_min_x, insert_max_x = unpack_mm_params(self.cr_conf['insert_x'])
        insert_min_y, insert_max_y = unpack_mm_params(self.cr_conf['insert_y'])

        img_h, img_w, _ = bg_img.shape

        fg_rect = generate_rect_coordinates(
            img_h=min(bg_img.shape[0], fg_img.shape[0]),
            img_w=min(bg_img.shape[1], fg_img.shape[1]),
            min_x=crop_min_x, min_y=crop_min_y,
            max_x=crop_max_x, max_y=crop_max_y,
            min_h=rect_min_h, min_w=rect_min_w,
            max_h=rect_max_h, max_w=rect_max_w,
        )

        x1, y1, x2, y2 = fg_rect
        cropped_img = fg_img[y1:y2, x1:x2]

        out_img, (shift_x, shift_y) = insert_image_in_background(
            bg_img, cropped_img, x1, y1,
            min_x=insert_min_x, min_y=insert_min_y,
            max_x=insert_max_x, max_y=insert_max_y,
        )

        fg_rect, fg_boxes = shift_fg_rect_and_boxes(fg_rect, fg_boxes, shift_x, shift_y)

        new_bg_boxes, new_bg_labels = correct_background_boxes(
            bg_boxes, bg_labels, fg_rect,
            self.pb_conf['max_overlap_area_ratio'],
            self.pb_conf['min_height_result_ratio'],
            self.pb_conf['min_width_result_ratio'],
            self.pb_conf['max_height_intersection'],
            self.pb_conf['max_width_intersection'],
        )

        new_fg_boxes, new_fg_labels = correct_foreground_boxes(
            fg_boxes, fg_labels, fg_rect,
            self.pb_conf['max_overlap_area_ratio'],
            self.pb_conf['min_height_result_ratio'],
            self.pb_conf['min_width_result_ratio'],
        )

        return out_img, \
            np.array(new_bg_boxes + new_fg_boxes, dtype=np.float32), \
            np.array(new_bg_labels + new_fg_labels)

    def __call__(self,
                 bg_img: np.array,
                 bg_boxes: np.array,
                 bg_labels: np.array,

                 fg_img: np.array,
                 fg_boxes: np.array,
                 fg_labels: np.array):

        return self.apply(bg_img, bg_boxes, bg_labels, fg_img, fg_boxes, fg_labels)
