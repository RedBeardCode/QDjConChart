#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File with sample responses of the Rest Server
"""
import responses

PRODUCT_GET_ARGS = (responses.GET, 'http://127.0.0.1:8000/api/')  # pylint: disable=E1101
PRODUCT_GET_KWARGS = {
    'body': '{"product": "http://127.0.0.1:8000/api/product/"}',
    'status': 200,
    'content_type': 'application/json'}
PRODUCT_LIST_GET_ARGS = (responses.GET, 'http://127.0.0.1:8000/api/product')  # pylint: disable=E1101
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
            '"measurement": "http://127.0.0.1:8000/api/measurement/"}',
    'status': 200,
    'content_type': 'application/json'}
PRODUCT_OPTIONS_ARGS = (responses.OPTIONS, 'http://127.0.0.1:8000/api/product')  # pylint: disable=E1101
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

MEAS_OPTIONS_ARGS = (responses.OPTIONS,  # pylint: disable=E1101
                     'http://127.0.0.1:8000/api/measurement')

MEAS_OPTIONS_KWARGS = {
    'body': """{
                "name": "Measurement Rest List",
                "description": "Rest view for the measurement model",
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
                        "date": {
                            "type": "datetime",
                            "required": true,
                            "read_only": false,
                            "label": "Date of the measurement"
                        },
                        "remarks": {
                            "type": "string",
                            "required": false,
                            "read_only": false,
                            "label": "Remarks"
                        },
                        "raw_data_file": {
                            "type": "file upload",
                            "required": true,
                            "read_only": false,
                            "label": "Raw data file"
                        },
                        "position": {
                            "type": "field",
                            "required": false,
                            "read_only": false,
                            "label": "Measurement position"
                        },
                        "altitude": {
                            "type": "decimal",
                            "required": false,
                            "read_only": false,
                            "label": "Altitude of the measurement"
                        },
                        "order": {
                            "type": "field",
                            "required": true,
                            "read_only": false,
                            "label": "Measurement order"
                        },
                        "examiner": {
                            "type": "field",
                            "required": true,
                            "read_only": false,
                            "label": "Examiner"
                        },
                        "meas_item": {
                            "type": "field",
                            "required": true,
                            "read_only": false,
                            "label": "Measurement item"
                        },
                        "measurement_tag": {
                            "type": "field",
                            "required": false,
                            "read_only": false,
                            "label": "Tag to distinguish the Measurements"
                        },
                        "order_items": {
                            "type": "field",
                            "required": true,
                            "read_only": false,
                            "label": "Item of the measurement order"
                        },
                        "measurement_devices": {
                            "type": "field",
                            "required": true,
                            "read_only": false,
                            "label": "Used measurement devices"
                        }
                    }
                }
            }""",
    'status': 200,
    'content_type': 'application/json'}


MEAS_LIST_GET_ARGS = (responses.GET, 'http://127.0.0.1:8000/api/measurement')  # pylint: disable=E1101
MEAS_LIST_GET_KWARGS = {
    'body': """
        [
            {
                "url": "http://127.0.0.1:8000/api/measurement/1/",
                "date": "2017-02-20T08:41:15.175283Z",
                "remarks": "length",
                "raw_data_file": "erste_messung_9h4Tqk1.txt",
                "position": "SRID=4326;POINT (7.24 50.08)",
                "altitude": "0.0",
                "order": "http://127.0.0.1:8000/api/measurementorder/1/",
                "examiner": "http://127.0.0.1:8000/api/user/1/",
                "meas_item": "http://127.0.0.1:8000/api/measurementitem/1/",
                "measurement_tag": null,
                "order_items": [
                    "http://127.0.0.1:8000/api/characteristicvaluedefinition/1/"
                ],
                "measurement_devices": [
                    "http://127.0.0.1:8000/api/measurementdevice/1/"
                ]
            },
            {
                "url": "http://127.0.0.1:8000/api/measurement/2/",
                "date": "2017-02-20T08:41:15.257732Z",
                "remarks": "length",
                "raw_data_file": "erste_messung_NAI5jKr.txt",
                "position": "SRID=4326;POINT (7.24 50.02)",
                "altitude": "0.0",
                "order": "http://127.0.0.1:8000/api/measurementorder/2/",
                "examiner": "http://127.0.0.1:8000/api/user/1/",
                "meas_item": "http://127.0.0.1:8000/api/measurementitem/2/",
                "measurement_tag": null,
                "order_items": [
                    "http://127.0.0.1:8000/api/characteristicvaluedefinition/1/"
                ],
                "measurement_devices": [
                    "http://127.0.0.1:8000/api/measurementdevice/1/"
                ]
            },
            {
                "url": "http://127.0.0.1:8000/api/measurement/3/",
                "date": "2017-02-20T08:41:15.297721Z",
                "remarks": "width",
                "raw_data_file": "erste_messung_oHparmO.txt",
                "position": "SRID=4326;POINT (7.29 50.23)",
                "altitude": "0.0",
                "order": "http://127.0.0.1:8000/api/measurementorder/2/",
                "examiner": "http://127.0.0.1:8000/api/user/1/",
                "meas_item": "http://127.0.0.1:8000/api/measurementitem/2/",
                "measurement_tag": null,
                "order_items": [
                    "http://127.0.0.1:8000/api/characteristicvaluedefinition/2/"
                ],
                "measurement_devices": [
                    "http://127.0.0.1:8000/api/measurementdevice/1/"
                ]
            }
        ]
        """,
    'status': 200,
    'content_type': 'application/json'}
