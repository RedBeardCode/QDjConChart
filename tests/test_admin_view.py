#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit test for creation of the admin view
"""
import responses
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


@responses.activate  # pylint: disable=E1101
def test_patch_object(qtbot):
    def check_patch(request):

        assert request.body == \
           b'{"altitude": 0.0, ' \
           b'"date": "2017-02-20T08:41:15.175283Z",' \
           b' "examiner": "Spam and Egg", ' \
           b'"meas_item": "http://127.0.0.1:8000/api/measurementitem/1/", ' \
           b'"measurement_devices": ' \
           b'["http://127.0.0.1:8000/api/measurementdevice/1/"], ' \
           b'"measurement_tag": null, ' \
           b'"order": "http://127.0.0.1:8000/api/measurementorder/1/", ' \
           b'"order_items": ["http://127.0.0.1:8000/api/' \
           b'characteristicvaluedefinition/1/"], ' \
           b'"position": "SRID=4326;POINT (7.24 50.08)", ' \
           b'"raw_data_file": "erste_messung_9h4Tqk1.txt", ' \
           b'"remarks": "length"}'
        return(200, '', request.body)
    responses.add_callback(responses.PATCH,  # pylint: disable=E1101
                           'http://127.0.0.1:8000/api/measurement/1/',
                           callback=check_patch)
    main_win = QMainWindow()
    AdminView(main_win, True)
    tablelist = main_win.findChild(TableList)
    qtbot.addWidget(main_win)
    tablelist.item(1).setSelected(True)
    table = main_win.findChild(QTableWidget, 'Measurement table')
    table.item(0, 2).setText('Spam and Egg')
