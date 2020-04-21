#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: __init__

:Synopsis:

:Author:
    servilla

:Created:
    4/12/20
"""
import os

import daiquiri

from webapp.config import Config


logger = daiquiri.getLogger(__name__)

path = Config.ROOT_DIR + "/static"
os.makedirs(path, exist_ok=True)
logger.info(f"Created root working directories: {Config.ROOT_DIR} and {path} ")
