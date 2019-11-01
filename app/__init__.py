import os

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY'),
        DATABASE = os.path.join(app.instance_path, 'defesa.db'),
        TEMPLATES_AUTO_RELOAD=True
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if not os.environ.get('MAP_KEY') or not os.environ.get('OPEN_KEY'):
        raise RuntimeError('MAP_KEY or OPEN_KEY not set')


    from . import alerta
    app.register_blueprint(alerta.bp)
    app.add_url_rule('/', endpoint='index')

    return app
