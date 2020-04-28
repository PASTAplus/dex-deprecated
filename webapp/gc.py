#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: gc

:Synopsis:
    Perform routine garbage collection of data and plot files as specified
    in Config.ROOT_DIR.

:Author:
    servilla

:Created:
    4/21/20
"""
import logging
import os
from pathlib import Path
import shutil

import daiquiri
import pendulum

from config import Config


cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + "/gc.log"
daiquiri.setup(level=logging.INFO, outputs=(daiquiri.output.File(logfile),))
logger = daiquiri.getLogger(__name__)


def dispose():
    now = pendulum.now(tz="UTC")
    logger.info(f"Removing stale files...")
    os.chdir(Config.ROOT_DIR)
    p = Path(".")
    for child in p.iterdir():
        if child.name != "static":
            stat = Path(child).stat()
            mod_time = pendulum.from_timestamp(stat.st_mtime)
            time_delta = now.diff(mod_time).in_minutes()
            if time_delta > Config.STALE:
                shutil.rmtree(child, ignore_errors=True)
                logger.warning(f"Removed directory: {child}")
    p = Path("static")
    for child in p.iterdir():
        stat = Path(child).stat()
        mod_time = pendulum.from_timestamp(stat.st_ctime)
        time_delta = now.diff(mod_time).in_minutes()
        if time_delta > Config.STALE:
            Path(child).unlink(missing_ok=True)
            logger.warning(f"Removed static file: {child}")


def main():
    dispose()


if __name__ == "__main__":
    main()
