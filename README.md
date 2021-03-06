# Joel's Simple URL Shortener

## Introduction

Joel's Simple URL Shortener is a fun web application built using Flask and PostgreSQL.

## Try it out

You can try out the URL Shortener at https://joelloong.com.

Some example URLs you can try to shorten:

    - https://joelloong.com
    - https://github.com/joloong/url-shortener
    - https://www.google.com

## Development

Setting Up

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Setting Up Database

```
flask db migrate
flask db upgrade
```

Creating .env in root folder

```
echo DATABASE_URL=<your-database-url> > .env
```

Starting Up Development Server

```
FLASK_APP=app.py FLASK_ENV=development flask run
```
