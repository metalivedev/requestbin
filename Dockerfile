FROM python:2-onbuild
ENTRYPOINT ["gunicorn", "--access-logfile", "access.log", "--worker-class", "gevent", "--workers", "1", "--max-requests", "1000", "requestbin:app"]

