#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: datatable

:Synopsis:

:Author:
    servilla

:Created:
    4/12/20
"""
import os
import shutil
import uuid

import daiquiri

from webapp.config import Config


logger = daiquiri.getLogger(__name__)


def write(file_path: str, file_name: str, table: str) -> str:
    unique = str(uuid.uuid4())
    path_spec = f"{Config.ROOT_DIR}/{unique}/{file_path}"
    os.makedirs(path_spec, exist_ok=True)
    file_spec = f"{path_spec}/{file_name}"
    with open(file_spec, "w") as f:
        f.write(table)
    logger.info(f"Created data file: {file_spec}")
    return file_spec


def read(file_spec: str) -> str:
    with open(file_spec, "r") as f:
        table = f.read()
    return table


def remove(file_spec: str):
    os.chdir(Config.ROOT_DIR)
    path_spec = file_spec[len(Config.ROOT_DIR) + 1 :]
    unique = path_spec.split("/")[0]
    shutil.rmtree(unique, ignore_errors=True)
