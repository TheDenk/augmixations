# -*- coding: utf-8 -*-
from .cutmix import Cutmix
from .cutout import Cutout
from .mixup import Mixup

__version__ = '0.2.21'

__all__ = ['Cutmix', 'Cutout', 'Mixup']
