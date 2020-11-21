# -*- coding: utf-8 -*-
import pytest

from augmixations.blots import HandWrittenBlot


@pytest.yield_fixture(scope='module')
def hand_written_blot():
    aug = HandWrittenBlot((0, 0), (0, 0), (0, 0), (0, 0), (0, 0), 1)
    yield aug
