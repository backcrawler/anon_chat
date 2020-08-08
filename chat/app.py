import tornado.web
import tornado.ioloop

from .routing import urlpatterns
from .settings import site_settings


def make_app():
    return tornado.web.Application(urlpatterns, **site_settings)


def run_server():
    app = make_app()
    app.listen(8885)
    tornado.ioloop.IOLoop.current().start()
