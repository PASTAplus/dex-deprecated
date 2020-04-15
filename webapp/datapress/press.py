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
import pandas as pd


class Press:
    def __init__(self, entity: dict):
        self._file_spec = entity["file_spec"]
        self._file_name = entity["file_name"]
        self._purl = entity["purl"]
        self._df = pd.read_csv(self._file_spec)
        self._head = self._get_head()
        self._keys = self._df.keys()
        self._dtypes = self._df.dtypes.items()

    @property
    def dtypes(self):
        return self._dtypes

    @property
    def file_name(self):
        return self._file_name

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

    def _get_head(self) -> str:
        html = self._df.head(n=20).to_html()
        html = html.replace("<td>", "<td style='text-align: center'>")
        html = html.replace("<table border=\"1\" class=\"dataframe\">",
                            "<table class='table'>")
        return html
