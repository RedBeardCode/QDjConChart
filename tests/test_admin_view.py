#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit test for creation of the admin view
"""

from PyQt5.QtWidgets import QMainWindow  # pylint: disable=E0611
from PyQt5.QtWidgets import QTableWidget  # pylint: disable=E0611

from gui.admin_view import TableList, AdminView


def test_tablelist(qtbot):
    main_win = QMainWindow()
    AdminView(main_win, True)
    tablelist = main_win.findChild(TableList)
    qtbot.addWidget(main_win)
    assert tablelist
    assert tablelist.count() == 2
    item = tablelist.item(0)
    assert item.text() == 'Product'
    item.setSelected(True)
    table = main_win.findChild(QTableWidget, 'Product table')
    assert table
    assert table.rowCount() == 3
    assert table.columnCount() == 1
    item = tablelist.item(1)
    assert item.text() == 'Measurement'
    item.setSelected(True)
    table = main_win.findChild(QTableWidget, 'Measurement table')
    assert table
    assert table.rowCount() == 3
    assert table.columnCount() == 11
