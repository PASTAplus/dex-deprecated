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
from pathlib import Path
import uuid

import daiquiri
from flask import Flask, render_template, send_file, session
from flask_bootstrap import Bootstrap
from requests.structures import CaseInsensitiveDict
import requests

from webapp.config import Config
from webapp.forms import Plot
from webapp.forms import Subset
from webapp.dex import datatable
from webapp.dex import dobject
from webapp.dex.dobject import Dobject
from webapp.dex import dplot


cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + "/views.log"
daiquiri.setup(
    level=logging.INFO, outputs=(daiquiri.output.File(logfile), "stdout",)
)


app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)


@app.route("/info")
def info():
    key = session["key"]
    entity = json.loads(key)
    touch(entity["file_spec"])
    dobj = Dobject(entity)
    head = f"{Config.HOST}/head"
    stats = f"{Config.HOST}/stats"
    return render_template("info.html", h=head, s=stats, dobj=dobj)


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
            key = (
                f'{{"file_spec": "{file_spec}", "file_name": "{file_name}", '
                f'"purl": "{purl}"}}'
            )
            session["key"] = key
            entity = json.loads(key)
            dobj = Dobject(entity)
            head = f"{Config.HOST}/head"
            stats = f"{Config.HOST}/stats"
            return render_template("info.html", h=head, s=stats, dobj=dobj)
        else:
            return f"Data not found at URL: {purl}", 404

    return "No data link provided in request!", 400


@app.route("/head")
def head():
    key = session.get("key")
    entity = json.loads(key)
    touch(entity["file_spec"])
    dobj = Dobject(entity)
    table = dobj.head
    return render_template("table.html", table=table)


@app.route("/keys")
def keys():
    file_spec = session.get("key")
    dobj = Dobject(file_spec)
    k = dobj.keys
    return render_template("keys.html", keys=k)


@app.route("/plot", methods=["GET", "POST"])
def plot():
    key = session["key"]
    entity = json.loads(key)
    touch(entity["file_spec"])
    dobj = Dobject(entity)
    choices = list()
    no = 0
    for key in dobj.keys:
        choices.append((no, key))
        no += 1
    form = Plot()
    form.x_attr.choices = choices
    form.y_attr.choices = choices
    if form.validate_on_submit():
        x_attr = form.x_attr.data
        date_x = form.x_date.data
        y_attr = form.y_attr.data
        df = dobj.plot([x_attr, y_attr], date_x)
        file_name = str(uuid.uuid4()) + ".html"
        file_spec = Config.ROOT_DIR + "/static/" + file_name
        dplot.plot_xy(df, date_x, file_spec)
        return render_template("plot.html", f=file_name)
    else:
        return render_template("plot_form.html", form=form, dobj=dobj)


@app.route("/stats")
def stats():
    key = session.get("key")
    entity = json.loads(key)
    touch(entity["file_spec"])
    dobj = Dobject(entity)
    table = dobj.stats
    return render_template("table.html", table=table)


@app.route("/subset", methods=["GET", "POST"])
def subset():
    key = session["key"]
    entity = json.loads(key)
    touch(entity["file_spec"])
    dobj = Dobject(entity)
    choices = list()
    no = 0
    for key in dobj.keys:
        choices.append((no, key))
        no += 1
    form = Subset()
    form.attributes.choices = choices
    if form.validate_on_submit():
        columns = form.attributes.data
        r_start = form.row_start.data
        r_end = form.row_end.data
        df = dobj.subset(columns, r_start, r_end)
        table = dobject.get_head(df, 20)
        with open(dobj.file_path + "/subset.tbl", "w") as f:
            f.write(table)
        head = f"{Config.HOST}/subset_head"
        return render_template("subset.html", df=df, h=head)
    else:
        form.row_start.data = 0
        form.row_end.data = dobj.rows
        return render_template("subset_form.html", form=form, dobj=dobj)


@app.route("/subset_head")
def subset_head():
    key = session.get("key")
    entity = json.loads(key)
    touch(entity["file_spec"])
    dobj = Dobject(entity)
    file_path = dobj.file_path
    with open(file_path + "/subset.tbl", "r") as f:
        table = f.read()
    return render_template("table.html", table=table)


@app.route("/download")
def download():
    key = session.get("key")
    entity = json.loads(key)
    touch(entity["file_spec"])
    dobj = Dobject(entity)
    file_path = dobj.file_path + "/subset.csv"
    return send_file(
        file_path,
        mimetype="text/csv",
        as_attachment=True,
        attachment_filename="subset.csv",
    )


@app.route("/view")
def view():
    key = session.get("key")
    return f"Session name: {key}"


def get_file_name(headers: CaseInsensitiveDict) -> str:
    file_name = str(uuid.uuid4()) + ".csv"
    content_disposition = headers.get("Content-Disposition")
    if content_disposition is not None:
        if "attachment;" in content_disposition:
            fn_directive = content_disposition.split(" ")[1]
            file_name = fn_directive.split("=")[1]
    return file_name


def get_package_id(purl: str) -> str:
    path_frags = purl.split("/")
    scope = path_frags[-4]
    identifier = path_frags[-3]
    revision = path_frags[-2]
    package_id = f"{scope}.{identifier}.{revision}"
    return package_id


def touch(file_spec: str):
    _ = file_spec.lstrip(Config.ROOT_DIR)
    unique = _.split("/")[0]
    Path(f"{Config.ROOT_DIR}/{unique}").touch(exist_ok=True)


if __name__ == "__main__":
    app.run()
