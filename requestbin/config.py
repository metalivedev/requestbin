import os, urlparse
DEBUG = True
REALM = os.environ.get('REALM', 'local')

APPLICATION_ROOT = os.environ.get('APPLICATION_ROOT', '/')
PREFERRED_URL_SCHEME = os.environ.get('APPLICATION_SCHEME', 'http')

AUTH_COOKIE_NAME = os.environ.get('AUTH_COOKIE_NAME', False)
AUTH_SECRET = os.environ.get('AUTH_SECRET', False)
AUTH_REDIRECT = os.environ.get('AUTH_REDIRECT', False)

PORT_NUMBER = 4000

FLASK_SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", "Xr/1xfL/tpVE7jD11Mh1V8XWbg1a2tho742UwCFLHOE=")

BIN_TTL = 48*3600
STORAGE_BACKEND = "requestbin.storage.memory.MemoryStorage"
MAX_RAW_SIZE = 1024*10
IGNORE_HEADERS = []
MAX_REQUESTS = 20
CLEANUP_INTERVAL = 3600

REDIS_URL = ""
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_DB = 9

REDIS_PREFIX = "requestbin"

LOGFILE = os.environ.get("LOGFILE", "app.log")

if REALM == 'prod':
    DEBUG = False

    FLASK_SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", FLASK_SESSION_SECRET_KEY)

    STORAGE_BACKEND = "requestbin.storage.redis.RedisStorage"

    REDIS_URL = os.environ.get("REDIS_URL")
    url_parts = urlparse.urlparse(REDIS_URL)
    REDIS_HOST = url_parts.hostname
    REDIS_PORT = url_parts.port
    REDIS_PASSWORD = url_parts.password
    REDIS_DB = url_parts.fragment




    IGNORE_HEADERS = """
X-Varnish
X-Forwarded-For
X-Heroku-Dynos-In-Use
X-Request-Start
X-Heroku-Queue-Wait-Time
X-Heroku-Queue-Depth
X-Real-Ip
X-Forwarded-Proto
X-Via
X-Forwarded-Port
""".split("\n")[1:-1]
