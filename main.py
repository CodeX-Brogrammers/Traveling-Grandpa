import logging

from aioalice import get_new_configured_app
from aiohttp.web_response import Response
from aiohttp import web

from settings import settings
from routes import dp
import middleware
import models

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


def prepare_app():
    app = get_new_configured_app(dispatcher=dp, path=settings.path)
    app.router.add_route("*", "/{tail:.*}", lambda _: Response(status=403))
    logging.info("Init database connection")
    app.on_startup.append(models.init_database)
    app.middlewares.extend((
        middleware.only_post_request_middleware,
        middleware.ping_request_middleware,
        middleware.log_middleware,
        middleware.session_state_middleware
    ))
    return app


def main():
    app = prepare_app()
    logging.info("Start application")
    web.run_app(app, host=settings.host, port=settings.port, loop=dp.loop)


if __name__ == '__main__':
    main()
else:
    app = prepare_app()

