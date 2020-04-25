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
from pathlib import Path, PurePath
import pickle

import daiquiri
import pandas as pd


logger = daiquiri.getLogger(__name__)


class Dobject:
    def __init__(self, entity: dict):
        self._file_spec = entity["file_spec"]
        self._file_name = entity["file_name"]
        self._file_path = str(PurePath(self._file_spec).parent)
        self._purl = entity["purl"]
        dobject_pkl = self._file_path + "/dobject.pkl"
        if Path(dobject_pkl).exists():
            with open(dobject_pkl, "rb") as f:
                dobject_dict = pickle.load(f)
            self._head = dobject_dict["head"]
            self._keys = dobject_dict["keys"]
            self._dtypes = dobject_dict["dtypes"]
            self._shape = dobject_dict["shape"]
            self._stats = dobject_dict["stats"]
            self._rows = dobject_dict["rows"]
            self._cols = dobject_dict["cols"]
        else:
            self._df = pd.read_csv(self._file_spec)
            self._head = get_head(self._df)
            self._keys = self._df.keys()
            self._dtypes = self._df.dtypes.items()
            self._shape = self._df.shape
            self._stats = get_stats(self._df)
            self._rows = self._shape[0]
            self._cols = self._shape[1]
            dobject_dict = {
                "head": self._head,
                "keys": self._keys,
                "dtypes": self._dtypes,
                "shape": self._shape,
                "stats": self._stats,
                "rows": self._rows,
                "cols": self._cols,
            }
            with open(dobject_pkl, "wb") as f:
                pickle.dump(dobject_dict, f)

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
        df = pd.read_csv(self._file_spec)
        df = df.iloc[r_start : r_end + 1, columns]
        df.to_csv(self._file_path + "/subset.csv", index=False, header=True)
        return df

    def plot(self, columns: list, date_x: bool):
        df = pd.read_csv(self._file_spec)
        df = df.iloc[:, columns]
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
    html = html.replace(
        '<table border="1" class="dataframe">', "<table class='table'>"
    )
    return html
