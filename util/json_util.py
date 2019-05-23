#!/usr/bin/env python
# -*- coding:utf8 -*-
import json


def to_json(obj):
    return json.dumps(obj, ensure_ascii=False)
