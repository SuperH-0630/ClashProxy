from flask import Blueprint, abort, send_file

from config import conf

clash = Blueprint("clash", __name__)


@clash.route("/<string:c>")
def download_page(c: str):
    if c != conf["DOWNLOAD_URL"]:
        return abort(404)

    try:
        return send_file(f"{conf['OUTPUT_FILE_NAME']}.yaml")
    except FileNotFoundError:
        return abort(404)
