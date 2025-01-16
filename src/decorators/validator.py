from functools import wraps

from flask import request, Response, jsonify
from pydantic import BaseModel


def get_response(result, status_code: int = 200):
    match result:
        case None:
            return jsonify(), status_code

        case schema if isinstance(schema, BaseModel):
            return jsonify(**schema.model_dump()), status_code

        case flask_response if isinstance(flask_response, Response):
            return flask_response, status_code

        case data, int(code):
            return get_response(data, code)

        case list(many_data) | tuple(many_data):
            if len(many_data) == 0:
                return jsonify([]), status_code
            if isinstance(many_data[0], BaseModel):
                return jsonify([schema.model_dump() for schema in many_data]), status_code
            return jsonify(many_data), status_code

        case _ as something:
            try:
                return jsonify(something), status_code
            except TypeError:
                raise TypeError(f'Unable to serialize {something}')


def validate():
    def decorator(func):
        annotations: dict = func.__annotations__
        body_schema = annotations.get('body')
        query_schema = annotations.get('query')

        @wraps(func)
        def wrapper(*args, **kwargs):
            if body_schema is not None:
                if not issubclass(body_schema, BaseModel):
                    raise TypeError('Parameter body must be pydantic schema.')
                kwargs['body'] = body_schema(**request.json)

            if query_schema is not None:
                if not issubclass(query_schema, BaseModel):
                    raise TypeError('Parameter query must be pydantic schema.')
                kwargs['query'] = query_schema(**request.args)

            result = func(*args, **kwargs)
            return get_response(result)

        return wrapper
    return decorator