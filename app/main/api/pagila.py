from flask import Blueprint, request, abort

from app.main.service.pagila import PagilaService

pagila_api = Blueprint('api', __name__)
pagila_service = PagilaService()

@pagila_api.route('/show-tables')
def show_tables():  # put application's code here
    try:
        t = pagila_service.get_tables()
        return {'tables': t.tables}, 200
    except Exception as e:
        return {'error': str(e)}, 500


@pagila_api.route('/backup-table', methods=["POST"])
def backup_table():  # put application's code here
    try:
        data = request.json
        b = pagila_service.backup_whole_table(data["table_name"])
        return {}, 200
    except Exception as e:
        return {'error': str(e)}, 500


@pagila_api.route('/_healthz', methods=["GET"])
def healthcheck():
    return {}, 200
