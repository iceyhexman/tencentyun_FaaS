#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json


class response(object):
    def __init__(self):
        self.resp = {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {},
            "body": ""
        }

    def html(self, value, headers={}, statusCode=200):
        self.resp['headers'] = dict({'Content-Type': 'text/html'}, **headers)
        self.resp['statusCode'] = statusCode
        self.resp['body'] = value
        return self.resp

    def json(self, value, headers={}, statusCode=200):
        self.resp['headers'] = dict({'Content-Type': 'text/json'}, **headers)
        self.resp['statusCode'] = statusCode
        self.resp["body"] = json.dumps(value)
        return self.resp


class event_handler(object):

    def __init__(self,event):
        self.__value={"path": event['path'],
                      "method": event['httpMethod'],
                      "queryString": event['queryString'],
                      "headers":event['headers'],
                      "body": str('body' in event and event['body']),
                      "full": event
                      }

    def __getitem__(self, item):
        return item in self.__value and self.__value[item]

    def json(self,encoding='utf-8'):
        return json.loads(self.__value['body'],encoding=encoding)


class hexlt_app(object):
    def __init__(self):
        self.routes = {}

    def route(self, path=None):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

    def run(self,request,resp):
        if request['path'] in self.routes:
            return self.routes[request['path']]()
        else:
            return resp.html("REQUEST_ERROR!",statusCode=200)

