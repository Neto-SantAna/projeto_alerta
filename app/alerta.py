import os
import click
import requests

from flask import(
    Blueprint, g, render_template, url_for, current_app
)
from flask.cli import with_appcontext
from cs50 import SQL


bp = Blueprint('alerta', __name__)


@bp.after_request
def after_request(response):
    response.headers['Cache-control'] = 'no-cache', 'no-store', 'must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'

    return response


@bp.route('/')
def index():
    db = SQL('sqlite:///' + current_app.config['DATABASE'])
    open_key = os.environ.get('OPEN_KEY')
    map_key = os.environ.get('MAP_KEY')

    weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?id=3390760&units=metric&appid={open_key}')
    code = weather.json()

    occurrences = db.execute("SELECT "
                             "ocorrencias.processo_numero as process, "
                             "vistorias.vistoria_risco AS risk, "
                             "chamados.latitude AS latitude, "
                             "chamados.longitude AS longitude, "
                             "lonas.colocacao_lona_metragem AS lona FROM ocorrencias "
                             "INNER JOIN vistorias ON vistorias.processo_numero = ocorrencias.processo_numero "
                             "INNER JOIN chamados ON chamados.processo_numero = vistorias.processo_numero "
                             "INNER JOIN lonas ON lonas.processo_numero = chamados.processo_numero "
                             "WHERE ocorrencias.processo_ocorrencia='Deslizamentos de Barreiras' "
                             "AND latitude!='' AND risk!='Não informado'")

    return render_template("index.html", map_key=map_key, occurrences=occurrences, code=code)


@bp.route('/emergency')
def emergency():
    return render_template('emergency.html')


@bp.route('/data')
def data():
    db = SQL('sqlite:///' + current_app.config['DATABASE'])
    occurrences = db.execute("SELECT "
                             "ocorrencias.processo_numero AS process, "
                             "vistorias.vistoria_risco AS risk, "
                             "chamados.solicitacao_endereco AS address, "
                             "lonas.colocacao_lona_metragem AS lona FROM ocorrencias "
                             "INNER JOIN vistorias ON vistorias.processo_numero = ocorrencias.processo_numero "
                             "INNER JOIN chamados ON chamados.processo_numero = vistorias.processo_numero "
                             "INNER JOIN lonas ON lonas.processo_numero = chamados.processo_numero "
                             "WHERE ocorrencias.processo_ocorrencia='Deslizamentos de Barreiras' "
                             "AND latitude!='' AND risk!='Não informado' ORDER BY risk DESC")

    return render_template("data.html", occurrences=occurrences)


@bp.route('/about')
def about():
    return render_template('about.html')
