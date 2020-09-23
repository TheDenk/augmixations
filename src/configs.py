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
    # Max possible box height overlap threshold. If height is overlapped more this threshold - box will be dropped.
    'min_height_ratio': 0.25,
    # Max possible box width overlap threshold. If width is overlapped more this threshold - box will be dropped.
    'min_width_ratio': 0.25,
    'min_height_when_overlap_ratio': 0.1,
    'min_width_when_overlap_ratio': 0.1,
}
