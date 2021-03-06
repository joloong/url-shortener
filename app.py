from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from urllib.parse import urlparse, urljoin
import string
import random

from exceptions.MissingKeyError import MissingKeyError
from exceptions.InvalidShortUrlError import InvalidShortUrlError
from config import Config
from models import db, UrlModel
from services import UrlService

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)
migrate = Migrate(app, db)

url_to_short_cache = {}
short_to_url_cache = {}


def custom_dict_get(data, key, default=None, exception=True):
    value = data.get(key, default)
    if not value and exception:
        raise MissingKeyError(key)
    else:
        return value


def short_url_generator(size=6):
    short_url = ''.join(random.SystemRandom().choices(
        string.ascii_uppercase + string.ascii_lowercase + string.digits, k=size))

    return short_url


def is_original_url_valid(original_url):
    final_url = urlparse(urljoin(original_url, "/"))
    is_valid = (all([final_url.scheme, final_url.netloc, final_url.path])
                and len(final_url.netloc.split(".")) > 1)

    return is_valid

def add_original_url(original_url):
    while True:
        try:
            short_url = short_url_generator()
            UrlService.add_url(short_url, original_url)
            return short_url
        except InvalidShortUrlError:
            continue

@ app.route("/", methods=["GET", "POST"])
def root_handler():
    if request.method == "GET":
        return render_template("index.html")

    # Create short url
    data = request.get_json() or request.form
    try:
        original_url = custom_dict_get(data, "url")
    except MissingKeyError:
        return {"status": "missing original url"}, 404

    if not is_original_url_valid(original_url):
        return {"status": "invalid original url"}, 404

    short_url = UrlService.get_short_from_original_url(original_url)
    if not short_url:
        short_url = add_original_url(original_url)

    return {
        "short_url": f"{request.base_url}{short_url}"
    }


@ app.route("/<short_url>", methods=["GET"])
def original_handler(short_url):
    if len(short_url) != 6:
        return {"status": "incorrect short url length"}, 404

    original_url = UrlService.get_original_from_short_url(short_url)
    if not original_url:
        return {"status": "missing original url"}, 404

    return redirect(original_url, code=302) 

if __name__ == '__main__':
    port = Config.PORT
    app.run(host='0.0.0.0', port=port)
