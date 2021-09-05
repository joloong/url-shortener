from models import db
from models.UrlModel import UrlModel


def get_original_from_short_url(short_url: str) -> str:
    result = db.session.query(UrlModel).filter(
        UrlModel.short_url == short_url).first()

    if not result:
        return None

    return result.original_url


def get_short_from_original_url(original_url: str) -> str:
    result = db.session.query(UrlModel).filter(
        UrlModel.original_url == original_url).first()

    if not result:
        return None

    return result.short_url


def add_url(short_url: str, original_url: str) -> str:
    if get_original_from_short_url(short_url):
        raise Exception(f"short_url ({short_url}) is already taken!")

    existing_short_url = get_short_from_original_url(original_url)
    if existing_short_url:
        return existing_short_url

    new_url = UrlModel(short_url, original_url)
    db.session.add(new_url)
    db.session.commit()

    return new_url.short_url
