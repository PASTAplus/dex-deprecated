#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: deml

:Synopsis:

:Author:
    servilla

:Created:
    4/28/20
"""
from lxml import etree

import requests


class Deml():
    def __init__(self, purl: str):
        self._eml = get_eml(purl)
        self._entity_root = get_entity_root(self._eml, purl)
        self._header_lines = get_header_lines(self._entity_root)
        self._footer_lines = get_footer_lines(self._entity_root)


def clean(text):
    return " ".join(text.split())


def get_eml(purl: str) -> str:
    path_frags = purl.split("/")
    path_frags[4] = "metadata"
    path_frags.pop()
    eml_url = "/".join(path_frags)
    eml = None
    r = requests.get(eml_url)
    if r.status_code == requests.codes.ok:
        eml = r.text
    return eml


def get_entity_root(eml: str, purl: str):
    root = etree.fromstring(eml.encode("utf-8"))
    dtables = root.findall("./dataset/dataTable")
    dtable = None
    for dtable in dtables:
        urls = dtable.findall("./physical/distribution/online/url")
        for url in urls:
            if clean(url.xpath("string()")) == purl:
                break
    return dtable


def get_header_lines(entity) -> int:
    header_lines = 0
    _ = entity.find("./physical/dataFormat/textFormat/numHeaderLines")
    if _ is not None:
        header_lines = clean(_.xpath("string()"))
    return int(header_lines)


def get_footer_lines(entity) -> int:
    footer_lines = 0
    _ = entity.find("./physical/dataFormat/textFormat/numFooterLines")
    if _ is not None:
        footer_lines = clean(_.xpath("string()"))
    return int(footer_lines)

