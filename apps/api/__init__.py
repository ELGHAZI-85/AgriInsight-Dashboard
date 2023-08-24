# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint

# url /api
blueprint = Blueprint(
    'api_blueprint',
    __name__,
    url_prefix='/api'
)
