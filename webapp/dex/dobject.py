#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: press

:Synopsis:

:Author:
    servilla

:Created:
    4/12/20
"""
from pathlib import PurePath

import pandas as pd

import daiquiri


logger = daiquiri.getLogger(__name__)


class Dobject:
    def __init__(self, entity: dict):
        self._file_spec = entity["file_spec"]
        self._file_name = entity["file_name"]
        self._file_path = str(PurePath(self._file_spec).parent)
        self._purl = entity["purl"]
        self._df = pd.read_csv(self._file_spec)
        self._head = get_head(self._df)
        self._keys = self._df.keys()
        self._dtypes = self._df.dtypes.items()
        self._shape = self._df.shape
        self._stats = get_stats(self._df)
        self._rows = self._shape[0]
        self._cols = self._shape[1]
        _ = PurePath(self._file_spec)

    @property
    def cols(self):
        return self._cols

    @property
    def dtypes(self):
        return self._dtypes

    @property
    def file_name(self):
        return self._file_name

    @property
    def file_path(self):
        return self._file_path

    @property
    def file_spec(self):
        return self._file_spec

    @property
    def head(self):
        return self._head

    @property
    def keys(self):
        return self._keys

    @property
    def purl(self):
        return self._purl

    @property
    def rows(self):
        return self._rows

    @property
    def shape(self):
        return self._shape

    @property
    def stats(self):
        return self._stats

    def subset(self, columns: list, r_start: int, r_end: int):
        df = self._df.iloc[r_start:r_end + 1, columns]
        df.to_csv(self._file_path + "/subset.csv", index=False, header=True)
        return df

    def plot(self, columns: list, date_x: bool):
        df = self._df.iloc[:, columns]
        if date_x:
            df[df.keys()[0]] = pd.to_datetime(df[df.keys()[0]])
        return df


def get_head(df, n=20) -> str:
    raw = df.head(n).to_html()
    html = htmlify(raw)
    return html


def get_stats(df) -> str:
    raw = df.describe().to_html()
    html = htmlify(raw)
    return html


def htmlify(raw: str) -> str:
    html = raw
    html = html.replace("<td>", "<td style='text-align: center'>")
    html = html.replace("<table border=\"1\" class=\"dataframe\">",
                        "<table class='table'>")
    return html
