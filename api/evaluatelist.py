#!/usr/bin/env python
# -*- coding:utf8 -*-

from flask_restful import Resource, request
from flask import jsonify
from ModelFunction import evaluate
import traceback
#from flask_jwt_extended import jwt_required  ##供身份认证使用
#from public import common   # 供日志系统使用

class RecommandAPI(Resource):
    # @jwt_required
    def post(self):
        ret = {'data': None, 'success': 0, 'message': ''}
        try:
            test = request.json['test']
            N = request.json['N']
            ret = evaluate.precision_recall(test,N)
        except Exception as e:
            traceback.print_exc()
            ret.update({"message": 'Happen Exception: ' + str(e)})
        # common.create_user_log(module_id=46, describe="update company", status=ret['success'], error=ret['message'])
        return jsonify(ret)