#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File with sample responses of the Rest Server
"""
import responses

PRODUCT_GET_ARGS = (responses.GET, 'http://test/api/')  # pylint: disable=E1101
PRODUCT_GET_KWARGS = {
    'body': '{"product": "http://127.0.0.1:8000/api/product/"}',
    'status': 200,
    'content_type': 'application/json'}
PRODUCT_LIST_GET_ARGS = (responses.GET, 'http://test/api/product')  # pylint: disable=E1101
PRODUCT_LIST_GET_KWARGS = {
    'body': """[
                {
                 "url":"http://127.0.0.1:8000/api/product/1/",
                 "product_name":"product1"
                },
                {
                 "url":"http://127.0.0.1:8000/api/product/2/",
                 "product_name":"product2"
                },
                {
                 "url":"http://127.0.0.1:8000/api/product/3/",
                 "product_name":"product3"
                }
               ]""",
    'status': 200,
    'content_type': 'application/json'}

PRODUCT_MEAS_GET_KWARGS = {
    'body': '{"product": "http://127.0.0.1:8000/api/product/",'
            '"measurement": "http://127.0.0.1:8000/api/product/"}',
    'status': 200,
    'content_type': 'application/json'}
PRODUCT_OPTIONS_ARGS = (responses.OPTIONS, 'http://test/api/product')  # pylint: disable=E1101
PRODUCT_OPTIONS_KWARGS = {
    'body': """{
                "name": "Product Rest List",
                "description": "Rest view for the product model",
                "renders": [
                            "application/json",
                            "text/html"
                           ],
                "parses": [
                           "application/json",
                           "application/x-www-form-urlencoded",
                           "multipart/form-data"
                          ],
                "actions": {
                            "POST": {
                                     "url": {
                                             "type": "field",
                                             "required": false,
                                             "read_only": true,
                                             "label": "Url"
                                            },
                                            "product_name": {
                                                "type": "string",
                                                "required": true,
                                                "read_only": false,
                                                "label": "Product name",
                                                "max_length": 30
                                            }
                                        }
                                    }
                            }
                """,
    'status': 200,
    'content_type': 'application/json'}
