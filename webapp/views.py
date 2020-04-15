#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: views

:Synopsis:

:Author:
    servilla

:Created:
    4/13/20
"""
import json
import logging
import os

import daiquiri
from flask import Flask, render_template, session
from flask_bootstrap import Bootstrap
from requests.structures import CaseInsensitiveDict
import requests

from webapp.config import Config
from webapp.datapress import datatable
from webapp.datapress.press import Press


cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + "/views.log"
daiquiri.setup(level=logging.INFO,
               outputs=(daiquiri.output.File(logfile), "stdout",))


app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)


@app.route("/clean")
def clean():
    file_spec = session.get("key")
    datatable.remove(file_spec)
    return "None"


@app.route("/info")
def info():
    file_spec = session.get("key")
    return render_template("info.html")


@app.route("/<path:purl>")
def index(purl: str = None):
    if purl is not None:
        if purl == "favicon.ico":
            return '<link rel="shortcut icon" href="about:blank">'
        r = requests.get(purl)
        if r.status_code == requests.codes.ok:
            file_name = get_file_name(r.headers)
            file_path = purl[8:]
            table = r.text
            file_spec = datatable.write(file_path, file_name, table)
            key = (f'{{"file_spec": "{file_spec}", "file_name": "{file_name}", '
                   f'"purl": "{purl}"}}')
            session["key"] = key
            entity = json.loads(key)
            p = Press(entity)
            h = "http://localhost:5000/head"
            return render_template("info.html", h=h, p=p)

    return "Got it!"


@app.route("/head")
def head():
    key = session.get("key")
    entity = json.loads(key)
    p = Press(entity)
    h = p.head
    return render_template("head.html", head=h)


@app.route("/keys")
def keys():
    file_spec = session.get("key")
    p = Press(file_spec)
    k = p.keys
    return render_template("keys.html", keys=k)


@app.route("/view")
def view():
    file_spec = session.get("key")
    return f"Session name: {file_spec}"


def get_file_name(headers: CaseInsensitiveDict) -> str:
    file_name = None
    content_disposition = headers.get("Content-Disposition")
    if content_disposition is not None:
        if "attachment;" in content_disposition:
            fn_directive = content_disposition.split(" ")[1]
            file_name = fn_directive.split("=")[1]
    return file_name


if __name__ == "__main__":
    app.run()
