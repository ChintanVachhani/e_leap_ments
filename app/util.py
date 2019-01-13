from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(statusCode, message=None):
    # payload = {'error': HTTP_STATUS_CODES.get(statusCode, 'Unknown error')}
    payload = {
        'message': 'Unknown error'
    }
    if message:
        payload['message'] = message
    res = jsonify(payload)
    res.status_code = statusCode
    return res


def success_response(statusCode, message, data=None):
    payload = {
        'message': message
    }
    if len(data) > 0:
        payload['data'] = data
    res = jsonify(payload)
    res.status_code = statusCode
    return res
