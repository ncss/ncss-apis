# NCSS APIs

Visit [http://localhost:5000/docs/](http://localhost:5000/docs/) or [http://apis.ncss.cloud/docs/](http://apis.ncss.cloud/docs/) for the Swagger api specification.


# Development

Install the requirements using [Poetry](https://python-poetry.org/):

```
$ poetry install
$ poetry run pytest
$ poetry run run.py
```

To deploy in production:

```
$ poetry run gunicorn --forwarded-allow-ips '*' --bind localhost:5001 --access-logfile - ncss_apis:app
```

and then run a reverse proxy to listen for HTTP/HTTPS.
