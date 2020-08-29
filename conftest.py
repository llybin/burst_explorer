# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pytest


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "record_mode": "once",
        "decode_compressed_response": True,
    }
