#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Testing the generation of the classes for the rest api
"""
import pytest
import responses
from generate_classes import get_provided_classes, get_class_meta, get_objects
from generate_classes import generate_classes
from .rest_responses import PRODUCT_GET_ARGS, PRODUCT_OPTIONS_ARGS
from .rest_responses import PRODUCT_GET_KWARGS, PRODUCT_OPTIONS_KWARGS
from .rest_responses import PRODUCT_MEAS_GET_KWARGS
from .rest_responses import PRODUCT_LIST_GET_ARGS, PRODUCT_LIST_GET_KWARGS


@responses.activate  # pylint: disable=E1101
def test_getting_classes():
    responses.add(*PRODUCT_GET_ARGS, **PRODUCT_MEAS_GET_KWARGS)  # pylint: disable=E1101
    classes = get_provided_classes('http://test/api/', 'me', 'you')
    assert classes == ['Product', 'Measurement']


@responses.activate  # pylint: disable=E1101
def test_getting_meta():
    responses.add(*PRODUCT_OPTIONS_ARGS,  # pylint: disable=E1101
                  **PRODUCT_OPTIONS_KWARGS)
    resp_meta = get_class_meta('http://test/api/', 'Product', 'me', 'you')
    meta = {'product_name': {'type': 'string', 'required': True,
                             'read_only': False, 'label': 'Product name',
                             'max_length': 30}}
    assert resp_meta == meta


@responses.activate  # pylint: disable=E1101
def test_create_classes():
    responses.add(*PRODUCT_GET_ARGS, **PRODUCT_GET_KWARGS)  # pylint: disable=E1101
    responses.add(*PRODUCT_OPTIONS_ARGS, **PRODUCT_OPTIONS_KWARGS)  # pylint: disable=E1101
    cls_names = generate_classes('http://test/api/', 'me', 'you')
    assert cls_names == ['Product']
    try:
        from generate_classes import Product
    except ImportError:
        pytest.fail('Class couldn´t imported')
    prod = Product()
    assert hasattr(prod, 'product_name')
    assert hasattr(prod, 'product_name_field')
    assert hasattr(prod, 'url')
    assert hasattr(prod.product_name_field, 'required')
    assert hasattr(prod.product_name_field, 'read_only')
    assert hasattr(prod.product_name_field, 'max_length')
    assert hasattr(prod.product_name_field, 'label')
    assert prod.product_name_field.label == 'Product name'
    assert prod.product_name_field.max_length == 30
    assert prod.product_name_field.required
    assert not prod.product_name_field.read_only
    with pytest.raises(ValueError):
        prod.product_name = "This string is longer than 30 characters"


@responses.activate  # pylint: disable=E1101
def test_get_objects():
    responses.add(*PRODUCT_LIST_GET_ARGS, **PRODUCT_LIST_GET_KWARGS)  # pylint: disable=E1101
    obj_list = get_objects('http://test/api/', 'Product', 'me', 'you')
    assert len(obj_list) == 3
    product_names = [obj.product_name for obj in obj_list]
    for i, obj in enumerate(obj_list):
        assert 'product{0}'.format(i+1) in product_names
        prod_index = obj.product_name[-1]
        assert obj.url == 'http://127.0.0.1:8000/api/product/{0}/'.format(
            prod_index)
