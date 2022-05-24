def handle_bad_request(e):
    return {'error': str(e)}, 500
