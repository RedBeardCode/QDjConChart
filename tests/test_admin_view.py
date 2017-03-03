#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit test for creation of the admin view
"""

from PyQt5.QtWidgets import QMainWindow  # pylint: disable=E0611
from PyQt5.QtWidgets import QTableWidget  # pylint: disable=E0611

from gui.admin_view import create_admin_view, TableList


def test_tablelist(qtbot):
    main_win = QMainWindow()
    create_admin_view(main_win, True)
    tablelist = main_win.findChild(TableList)
    qtbot.addWidget(main_win)
    assert tablelist
    assert tablelist.count() == 1
    item = tablelist.item(0)
    assert item.text() == 'Product'
    item.setSelected(True)
    table = main_win.findChild(QTableWidget, 'Product table')
    assert table
