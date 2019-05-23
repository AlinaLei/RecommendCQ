#!/usr/bin/env python
# -*- coding:utf8 -*-
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from .evaluatelist import *

app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['JSON_AS_ASCII'] = False

#
api.add_resource(RecommandAPI, '/user/recommand/', endpoint='user_recommand')