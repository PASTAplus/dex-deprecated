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
import uuid

import daiquiri
from flask import Flask, render_template, send_file, session
from flask_bootstrap import Bootstrap
from requests.structures import CaseInsensitiveDict
import requests

from webapp.config import Config
from webapp.forms import Subset
from webapp.datapress import datatable
from webapp.datapress import press
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
    key = session["key"]
    entity = json.loads(key)
    p = Press(entity)
    head = f"{Config.HOST}/head"
    stats = f"{Config.HOST}/stats"
    return render_template("info.html", h=head, s=stats, p=p)


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
            head = f"{Config.HOST}/head"
            stats = f"{Config.HOST}/stats"
            return render_template("info.html", h=head, s=stats, p=p)

    return "Got it!"


@app.route("/head")
def head():
    key = session.get("key")
    entity = json.loads(key)
    p = Press(entity)
    table = p.head
    return render_template("table.html", table=table)


@app.route("/keys")
def keys():
    file_spec = session.get("key")
    p = Press(file_spec)
    k = p.keys
    return render_template("keys.html", keys=k)


@app.route("/stats")
def stats():
    key = session.get("key")
    entity = json.loads(key)
    p = Press(entity)
    table = p.stats
    return render_template("table.html", table=table)


@app.route("/subset", methods=['GET', 'POST'])
def subset():
    key = session["key"]
    entity = json.loads(key)
    p = Press(entity)
    choices = list()
    no = 0
    for key in p.keys:
        choices.append((no, key))
        no += 1
    form = Subset()
    form.attributes.choices = choices
    if form.validate_on_submit():
        columns = form.attributes.data
        r_start = form.row_start.data
        r_end = form.row_end.data
        df = p.subset(columns, r_start, r_end)
        table = press.get_head(df, 5)
        return render_template("subset_download.html", df=df, table=table)
    else:
        form.row_start.data = 0
        form.row_end.data = p.rows
        return render_template("subset.html", form=form, p=p)
    return ""


@app.route("/download")
def download():
    key = session.get("key")
    entity = json.loads(key)
    p = Press(entity)
    file_path = p.file_path + "/subset.csv"
    return send_file(file_path,
                     mimetype="text/csv",
                     as_attachment=True,
                     attachment_filename="subset.csv")


@app.route("/view")
def view():
    file_spec = session.get("key")
    return f"Session name: {file_spec}"


def get_file_name(headers: CaseInsensitiveDict) -> str:
    file_name = str(uuid.uuid4()) + ".csv"
    content_disposition = headers.get("Content-Disposition")
    if content_disposition is not None:
        if "attachment;" in content_disposition:
            fn_directive = content_disposition.split(" ")[1]
            file_name = fn_directive.split("=")[1]
    return file_name


if __name__ == "__main__":
    app.run()
