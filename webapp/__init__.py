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

from webapp.config import Config


os.makedirs(Config.ROOT_DIR + "/static", exist_ok=True)
