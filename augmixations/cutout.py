# -*- coding: utf-8 -*-
import numpy as np

from .utils import unpack_mm_params, generate_parameter
from .configs import cutout_process_box_config, cutout_crop_rect_config
from .core import (
    generate_rect_coordinates,
    correct_background_boxes,
)


class SmartCutout:
    """
    Description:
    CutOut class. This class allows crop part of image and fill this place some color.
    It also changes boxes and labels.

    Init Parameters:

    crop_rect_config (dict) - Config with parameters of cut and insert coordinates
    process_boxes_config (dict) - Config with parameters of maximum box area overlap and maximum box side overlap
    """

    def __init__(self, crop_rect_config: dict = None,
                 process_boxes_config: dict = None,):
        self.cr_conf = cutout_crop_rect_config if crop_rect_config is None else crop_rect_config
        self.pb_conf = cutout_process_box_config if process_boxes_config is None else process_boxes_config

        for def_key, def_val in cutout_crop_rect_config.items():
            if def_key not in self.cr_conf.keys() or self.cr_conf[def_key] is None:
                self.cr_conf[def_key] = def_val

        for def_key, def_val in cutout_process_box_config.items():
            if def_key not in self.pb_conf.keys() or self.pb_conf[def_key] is None:
                self.pb_conf[def_key] = def_val

    def apply(self,
              img: np.array,
              boxes: np.array,
              labels: np.array):
        """
        Description:
        CutOut function. It function crop part of image from second image and paste it into first image.
        Function also changes first and second boxes and labels.

        Parameters:

        img (np.array) - Background image. The image into which another image will be inserted.
        boxes (np.array) - Boxes for background image.
        labels (np.array) - Labels for background image.

        Return:
        (new_image, new_boxes, new_labels) - New image, boxes and labels
        """
        crop_min_x, crop_max_x = unpack_mm_params(self.cr_conf['crop_x'])
        crop_min_y, crop_max_y = unpack_mm_params(self.cr_conf['crop_y'])
        rect_min_h, rect_max_h = unpack_mm_params(self.cr_conf['rect_h'])
        rect_min_w, rect_max_w = unpack_mm_params(self.cr_conf['rect_w'])
        min_transp, max_transp = unpack_mm_params(self.cr_conf['transparency'])
        min_holes, max_holes = unpack_mm_params(self.cr_conf['hole_nums'])
        holes = generate_parameter(min_holes, max_holes)

        new_boxes = boxes.copy()
        new_labels = labels.copy()
        out_img = img.copy()

        for _ in range(holes):
            rect = generate_rect_coordinates(
                img_h=img.shape[0],
                img_w=img.shape[1],
                min_x=crop_min_x, min_y=crop_min_y,
                max_x=crop_max_x, max_y=crop_max_y,
                min_h=rect_min_h, min_w=rect_min_w,
                max_h=rect_max_h, max_w=rect_max_w,
            )

            x1, y1, x2, y2 = rect
            transp = generate_parameter(min_transp, max_transp)

            out_img[y1:y2, x1:x2:, :] = (out_img[y1:y2, x1:x2:, :] * transp).astype(np.uint8)

            if transp < self.pb_conf['transp_box_visibility']:
                new_boxes, new_labels = correct_background_boxes(
                    new_boxes, new_labels, rect,
                    self.pb_conf['max_overlap_area_ratio'],
                    self.pb_conf['min_height_result_ratio'],
                    self.pb_conf['min_width_result_ratio'],
                    self.pb_conf['max_height_intersection'],
                    self.pb_conf['max_width_intersection'],
                )

        return out_img, \
            np.array(new_boxes, dtype=np.float32), \
            np.array(new_labels)

    def __call__(self,
                 img: np.array,
                 boxes: np.array,
                 labels: np.array,):

        return self.apply(img, boxes, labels)
