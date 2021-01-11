# -*- coding: utf-8 -*-
from .cutmix import SmartCutmix
from .blots import HandWrittenBlot
from .cutout import SmartCutout

__version__ = '0.1.1'

__all__ = ['SmartCutmix', 'HandWrittenBlot', 'SmartCutout']
