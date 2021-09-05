from models import db


class UrlModel(db.Model):
    __tablename__ = 'urls'

    short_url = db.Column(db.String(6), primary_key=True)
    original_url = db.Column(db.String(), nullable=False)

    __table_args__ = (
        db.UniqueConstraint(original_url),
    )

    def __init__(self, short_url, original_url):
        self.short_url = short_url
        self.original_url = original_url

    def __repr__(self):
        return f"<Url {self.short_url} {self.original_url}>"

    def serialize(self):
        return {
            "short_url": self.short_url,
            "original_url": self.original_url
        }
