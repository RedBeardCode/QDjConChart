#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create the view to administrate the db classes
"""
import responses
from PyQt5.QtCore import Qt  # pylint: disable=E0611

from PyQt5.QtWidgets import QDockWidget  # pylint: disable=E0611
from PyQt5.QtWidgets import QListWidget  # pylint: disable=E0611
from PyQt5.QtWidgets import QTableWidget  # pylint: disable=E0611

from generate_classes import generate_classes
from tests.rest_responses import PRODUCT_GET_KWARGS, PRODUCT_GET_ARGS
from tests.rest_responses import PRODUCT_OPTIONS_KWARGS, PRODUCT_OPTIONS_ARGS
from settings import API_PWD, API_URL, API_USER


class TableList(QListWidget):
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
        self.itemSelectionChanged.connect(self.update_view)

    def add_available_tables(self):
        """
        Fills available tables in the list widget
        :param list: List widget
        """
        for cls_name in self.table_cls_names:
            self.addItem(cls_name)

    def update_view(self):
        """
        After selecting a table the new Widget for the table will be created
        """
        item = self.selectedItems()[0]
        print(item)


def create_admin_view(parent, use_debug_server=False):
    """
    Creates the gui objects for the admin view
    :param parent: Parent window
    """
    table = QTableWidget(parent)
    parent.setCentralWidget(table)
    list_dock = QDockWidget("Select Table", parent)
    list_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
    tab_list = TableList(list_dock, use_debug_server=use_debug_server)
    list_dock.setWidget(tab_list)
    parent.addDockWidget(Qt.LeftDockWidgetArea, list_dock)
