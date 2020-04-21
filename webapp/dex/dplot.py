#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: dplot

:Synopsis:

:Author:
    servilla

:Created:
    4/21/20
"""
import os

from bokeh.plotting import figure, output_file, save, show
from bokeh.models import ColumnDataSource
import daiquiri

from webapp.config import Config


logger = daiquiri.getLogger(__name__)


def plot_xy(df, date_x: bool, file_spec: str):
    os.makedirs(Config.ROOT_DIR + "/static", exist_ok=True)
    output_file(file_spec)
    if date_x:
        p = figure(x_axis_type='datetime')
    else:
        p = figure()
    p.xaxis.axis_label = df.keys()[0]
    p.yaxis.axis_label = df.keys()[1]
    source = ColumnDataSource(df)
    p.circle(x=df.keys()[0], y=df.keys()[1], source=source)
    save(p)
    logger.info(f"Created plot file: {file_spec}")
