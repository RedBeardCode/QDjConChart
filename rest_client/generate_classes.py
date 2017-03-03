#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generating the classes for the provides Models from the rest api
"""
from types import new_class

from requests import get, options


class RestBase(object):  # pylint: disable=R0903
    """
    Base class for the for the rest api tables generated classes
    """
    def __init__(self, *_, **kwargs):
        self.__url = kwargs.pop('url', '')
        for field_name in self.meta:  # pylint: disable=E1101
            field = FIELDS[self.meta[field_name]['type']](  # pylint: disable=E1101
                **self.meta[field_name])  # pylint: disable=E1101
            setattr(self, field_name + '_field', field)
            setattr(
                self.__class__, field_name,
                property(
                    lambda self, fna=field_name:
                        getattr(self, fna + '_field').get(),  # pylint: disable=W0640
                    lambda self, v, fna=field_name:
                        getattr(self, fna + '_field').set(v)  # pylint: disable=W0640
                )
            )
        for key in kwargs:
            setattr(self, key, kwargs[key])

    @property
    def url(self):
        """
        Url to the REST Object
        """
        return self.__url


class Field(object):
    """
    Base class for all field defined form the rest api
    """
    def __init__(self, *_, **kwargs):
        self.__label = kwargs['label']
        self.__required = kwargs['required']
        self.__read_only = kwargs['read_only']
        self.yvalue = None

    @property
    def label(self):
        """
        Label of the field (read only)
        """
        return self.__label

    @property
    def required(self):
        """
        Is this field required (read only)
        """
        return self.__required

    @property
    def read_only(self):
        """
        Is this field read only (read only)
        """
        return self.__read_only

    def get(self):
        """
        Returns the field value
        """
        return self.yvalue

    def set(self, value):
        """
        Sets the field value
        """
        self.yvalue = value


class StringField(Field):  # pylint: disable=R0903
    """
    Class for rest string fields
    """
    def __init__(self, *args, **kwargs):
        super(StringField, self).__init__(*args, **kwargs)
        self.__max_length = kwargs.get('max_length', 2048)

    @property
    def max_length(self):
        """
        Max length of the string (read-only)
        """
        return self.__max_length

    def set(self, value):
        """
        Set the string value if the value isn't too long
        :param value: New sting
        """
        if len(value) > self.max_length:
            raise ValueError("String is to long")
        self.yvalue = value


class DateTime(Field):
    """
    Class for datetime field
    """
    def __init__(self, *args, **kwargs):
        super(DateTime, self).__init__(*args, **kwargs)


class FloatField(Field):
    """
    Class for float fields
    """
    def __init__(self, *args, **kwargs):
        super(FloatField, self).__init__(*args, **kwargs)

    def set(self, value):
        """
        Set the float value if it isn't able to convert to float a exception is
        raised
        :param value: New value
        """
        self.yvalue = float(value)


FIELDS = {'string': StringField,
          'datetime': DateTime,
          'field': Field,
          'file upload': Field,
          'decimal': FloatField,
          }


def get_provided_classes(rooturl, user, pwd):
    """
    Reads the with classes are available over the rest api
    :param rooturl: Url of the rest api
    :return: list of class names
    """
    response = get(rooturl, auth=(user, pwd))
    cls_names = []
    for name in response.json().keys():
        cls_names.append(name.capitalize())
    return cls_names


def get_class_meta(rooturl, clsname, user, pwd):
    """
    Read the meta data of the given class from the rest api
    :param rooturl: Base url of the rest api
    :param clsname: Name of the class
    :param user: User name to authenticate at the rest api
    :param pwd: Password name to authenticate at the rest api
    :return: Dict with class meta data
    """
    url = __combine_url(rooturl, clsname)
    resp_opt = options(url, auth=(user, pwd))
    resp_dict = resp_opt.json()
    meta_data = resp_dict['actions']['POST']
    meta_data.pop('url')
    return meta_data


def __combine_url(rooturl, clsname):
    """
    Creates the full url out of rooturl and class name
    :param rooturl: Base url of the rest api
    :param clsname: Class name
    :return:
    """
    url = rooturl
    if url[-1] != '/':
        url += '/'
    url += clsname.lower()
    return url


def generate_classes(rooturl, user, pwd):
    """
    Generates classes for from rest api given structs. After the classes are
    generated they can be imported like normal classes
    :param rooturl: URL to rest api
    :param user: Username for the Rest API
    :param pwd: Password of the Rest API
    :return: A List with class names
    """
    cls_names = get_provided_classes(rooturl, user, pwd)
    for name in cls_names:
        meta = get_class_meta(rooturl, name, user, pwd)
        cls = new_class(name, (RestBase,))
        setattr(cls, 'meta', meta)
        globals()[name] = cls
    return cls_names


def get_objects(rooturl, clsname, user, pwd):
    """
    Reads the db entries from the rest api and returns a list of objects for
    each entry
    :param rooturl: base url of the rest api
    :param clsname: class name for witch the entries should be fetch
    :param user: Username for the Rest API
    :param pwd: Password of the Rest API
    :return: A list of objects for each db entry
    """
    url = __combine_url(rooturl, clsname)
    response = get(url, auth=(user, pwd))
    resp_list = response.json()
    cls = globals()[clsname]
    obj_list = []
    for kwargs in resp_list:
        obj_list.append(cls(**kwargs))
    return obj_list
