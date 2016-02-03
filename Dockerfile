FROM python:2-onbuild
ENTRYPOINT ["gunicorn", "--worker-class", "gevent", "--workers", "2", "--max-requests", "1000", "requestbin:app"]

