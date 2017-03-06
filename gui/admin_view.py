#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create the view to administrate the db classes
"""
import responses
from PyQt5.QtCore import Qt  # pylint: disable=E0611
from PyQt5.QtCore import QObject  # pylint: disable=E0611
from PyQt5.QtWidgets import QDockWidget  # pylint: disable=E0611
from PyQt5.QtWidgets import QListWidget  # pylint: disable=E0611
from PyQt5.QtWidgets import QTableWidget  # pylint: disable=E0611
from PyQt5.QtWidgets import QTableWidgetItem  # pylint: disable=E0611

from rest_client.generate_classes import generate_classes, get_objects
from settings import API_PWD, API_URL, API_USER
from tests.rest_responses import PRODUCT_GET_ARGS
from tests.rest_responses import PRODUCT_MEAS_GET_KWARGS
from tests.rest_responses import PRODUCT_OPTIONS_KWARGS, PRODUCT_OPTIONS_ARGS
from tests.rest_responses import PRODUCT_LIST_GET_ARGS, PRODUCT_LIST_GET_KWARGS
from tests.rest_responses import MEAS_OPTIONS_ARGS, MEAS_OPTIONS_KWARGS
from tests.rest_responses import MEAS_LIST_GET_ARGS, MEAS_LIST_GET_KWARGS


class RequestMock(responses.RequestsMock):
    """
    Wrapper around responses.RequestMock to make it easy to enalbe/disable the
    debug_server
    """
    def __init__(self, use_debug_server, *args,
                 assert_all_requests_are_fired=False, **kwargs):
        self.__use_debug_server = use_debug_server
        super(RequestMock, self).__init__(
            *args, assert_all_requests_are_fired=assert_all_requests_are_fired,
            **kwargs)

    def __enter__(self):
        if self.__use_debug_server:
            super(RequestMock, self).__enter__()
        return self

    def __exit__(self, *args):
        if self.__use_debug_server:
            super(RequestMock, self).__exit__(*args)


class TableList(QListWidget):  # pylint: disable=R0903
    """
    Widget which shows a list of all table of the REST API
    """

    def __init__(self, *args, **kwargs):
        self.__use_debug_server = kwargs.pop('use_debug_server', False)
        super(TableList, self).__init__(*args, **kwargs)
        with RequestMock(self.__use_debug_server) as rsps:
            rsps.add(*PRODUCT_GET_ARGS,
                     **PRODUCT_MEAS_GET_KWARGS)
            rsps.add(*PRODUCT_OPTIONS_ARGS,
                     **PRODUCT_OPTIONS_KWARGS)
            rsps.add(*MEAS_OPTIONS_ARGS,
                     **MEAS_OPTIONS_KWARGS)
            self.table_cls_names = generate_classes(API_URL, API_USER, API_PWD)
            self.add_available_tables()

    def add_available_tables(self):
        """
        Fills available tables in the list widget
        :param list: List widget
        """
        for cls_name in self.table_cls_names:
            self.addItem(cls_name)


class AdminView(QObject):
    """
    Class representing the admin view with the dockable table list and the
    table widget
    """
    def __init__(self, parent, use_debug_server=False):
        super(AdminView, self).__init__(parent)
        self.__parent = parent
        self.__use_debug_server = use_debug_server
        self.__current_table = QTableWidget(parent)
        parent.setCentralWidget(self.__current_table)
        list_dock = QDockWidget("Select Table", parent)
        list_dock.setAllowedAreas(
            Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.__tab_list = TableList(list_dock,
                                    use_debug_server=use_debug_server)
        self.__tab_list.itemSelectionChanged.connect(self.update_view)
        self.__column_fields = []
        list_dock.setWidget(self.__tab_list)
        parent.addDockWidget(Qt.LeftDockWidgetArea, list_dock)

    def update_view(self):
        """
        After selecting a table the new Widget for the table will be created
        """
        self.__current_table.deleteLater()
        item = self.__tab_list.selectedItems()[0]
        self.create_table(item)

    def create_table(self, item):
        """
        Creates the filled table for the selected item
        :param item: Selected item
        """
        with RequestMock(self.__use_debug_server) as rsps:
            rsps.add(*PRODUCT_LIST_GET_ARGS,
                     **PRODUCT_LIST_GET_KWARGS)
            rsps.add(*MEAS_LIST_GET_ARGS,
                     **MEAS_LIST_GET_KWARGS)
            objects = get_objects(API_URL, item.text(), API_USER, API_PWD)
            tab_name = '{0} table'.format(item.text())
            members = objects[0].get_fields()
            self.__current_table = QTableWidget(len(objects),
                                                len(members),
                                                self.__parent,
                                                objectName=tab_name)
            self.__column_fields = []
            for i, obj in enumerate(objects):
                for j, mem in enumerate(members):
                    field = getattr(obj, mem + '_field')
                    if i == 0:
                        label = field.label
                        self.__current_table.setHorizontalHeaderItem(
                            j, QTableWidgetItem(label))
                        self.__column_fields.append(mem)
                    value = getattr(obj, mem)
                    if isinstance(value, list):
                        value = '\n'.join(value)
                    table_item = QTableWidgetItem(value)
                    table_item.setData(Qt.UserRole, obj)
                    if field.read_only:
                        table_item.setFlags(Qt.ItemIsEnabled)
                    self.__current_table.setItem(i, j, table_item)
            self.__current_table.itemChanged.connect(self.item_changed)
            self.__parent.setCentralWidget(self.__current_table)

    def item_changed(self, item):
        """
        Sends the changes back to the server
        """
        obj = item.data(Qt.UserRole)
        setattr(obj, self.__column_fields[item.column()], item.text())
        obj.patch()
