# -*- coding: utf-8 -*-
crop_rect_config_default = {
    'crop_min_x': None,
    'crop_max_x': None,

    'crop_min_y': None,
    'crop_max_y': None,

    'min_rect_h': None,
    'max_rect_h': None,

    'min_rect_w': None,
    'max_rect_w': None,

    'insert_min_x': None,
    'insert_max_x': None,

    'insert_min_y': None,
    'insert_max_y': None,
}

process_box_config_default = {
    # Max possible box overlap area threshold. If overlap part more this threshold - box will be dropped.
    'max_overlap_area_ratio': 0.75,

    'min_height_result_ratio': 0.25,
    'min_width_result_ratio': 0.25,

    'max_height_intersection': 0.9,
    'max_width_intersection': 0.9,
}
