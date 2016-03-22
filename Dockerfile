FROM python:2-onbuild
ENTRYPOINT ["gunicorn", "--worker-class", "gevent", "--workers", "1", "--max-requests", "1000", "requestbin:app"]

