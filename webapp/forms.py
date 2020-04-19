#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: forms

:Synopsis:

:Author:
    servilla

:Created:
    4/17/20
"""
from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import DateField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import SelectMultipleField
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import Optional

from webapp.dex.dobject import Dobject


class Subset(FlaskForm):
    attributes = SelectMultipleField("Attributes", coerce=int)
    row_start = IntegerField("Row Start")
    row_end = IntegerField("Row End")


class Plot(FlaskForm):
    x_attr = SelectField("X Attribute", coerce=int)
    x_date = BooleanField("X is date")
    y_attr = SelectField("Y Attribute", coerce=int)
