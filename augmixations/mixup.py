# -*- coding: utf-8 -*-
import numpy as np

from .utils import generate_parameter, unpack_mm_params


class Mixup:
    def __init__(self, transparency=(0.4, 0.6)):
        self.min_t, self.max_t = unpack_mm_params(transparency)

    def apply(self,
              bg_img: np.array,
              bg_boxes: np.array,
              bg_labels: np.array,

              fg_img: np.array,
              fg_boxes: np.array,
              fg_labels: np.array):
        if bg_img.shape != fg_img.shape:
            raise Exception('Both input images should be equal shape. \
            Current shapes: bg_img {bg_img.shape}, fg_img {fg_img.shape}')

        transp = generate_parameter(self.min_t, self.max_t, 'transparency')

        bg = bg_img.copy().astype(float)
        fg = fg_img.copy().astype(float)

        image = bg * transp + fg * (1 - transp)
        image = np.clip(image, 0, 255).astype(np.uint8)

        boxes = np.vstack([bg_boxes, fg_boxes])
        labels = np.hstack([bg_labels, fg_labels])

        return image, boxes, labels

    def __call__(self,
                 bg_img: np.array,
                 bg_boxes: np.array,
                 bg_labels: np.array,

                 fg_img: np.array,
                 fg_boxes: np.array,
                 fg_labels: np.array):

        return self.apply(bg_img, bg_boxes, bg_labels, fg_img, fg_boxes, fg_labels)
