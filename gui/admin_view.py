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
from tests.rest_responses import PRODUCT_GET_KWARGS, PRODUCT_GET_ARGS
from tests.rest_responses import PRODUCT_OPTIONS_KWARGS, PRODUCT_OPTIONS_ARGS
from tests.rest_responses import PRODUCT_LIST_GET_ARGS, PRODUCT_LIST_GET_KWARGS


class TableList(QListWidget):  # pylint: disable=R0903
    """
    Widget which shows a list of all table of the REST API
    """
    @responses.activate  # pylint: disable=E1101
    def __init__(self, *args, **kwargs):
        self.__use_debug_server = kwargs.pop('use_debug_server', False)
        super(TableList, self).__init__(*args, **kwargs)
        if self.__use_debug_server:
            responses.add(*PRODUCT_GET_ARGS,   # pylint: disable=E1101
                          **PRODUCT_GET_KWARGS)
            responses.add(*PRODUCT_OPTIONS_ARGS,   # pylint: disable=E1101
                          **PRODUCT_OPTIONS_KWARGS)
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
        list_dock.setWidget(self.__tab_list)
        parent.addDockWidget(Qt.LeftDockWidgetArea, list_dock)

    def update_view(self):
        """
        After selecting a table the new Widget for the table will be created
        """
        self.__current_table.deleteLater()
        item = self.__tab_list.selectedItems()[0]
        self.create_table(item)

    @responses.activate  # pylint: disable=E1101
    def create_table(self, item):
        """
        Creates the filled table for the selected item
        :param item: Selected item
        """
        if self.__use_debug_server:
            responses.add(*PRODUCT_LIST_GET_ARGS,   # pylint: disable=E1101
                          **PRODUCT_LIST_GET_KWARGS)
        objects = get_objects(API_URL, item.text(), API_USER, API_PWD)
        tab_name = '{0} table'.format(item.text())
        members = [mem for mem in dir(objects[0]) if not mem.startswith('_')
                   and mem not in ['meta', 'url']
                   and not mem.endswith('_field')]
        self.__current_table = QTableWidget(len(objects),
                                            len(members),
                                            self.__parent,
                                            objectName=tab_name)
        self.__current_table.setHorizontalHeaderLabels(members)
        for i, obj in enumerate(objects):
            for j, mem in enumerate(members):
                value = getattr(obj, mem)
                item = QTableWidgetItem(value)
                item.setFlags(Qt.ItemIsEnabled)
                self.__current_table.setItem(i, j, item)
        self.__parent.setCentralWidget(self.__current_table)


def create_admin_view(parent, use_debug_server=False):
    """
    Creates the gui objects for the admin view
    :param parent: Parent window
    """
    _ = AdminView(parent, use_debug_server)
