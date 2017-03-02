#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main app to start the gui
"""
import argparse

from PyQt5.QtWidgets import QApplication  # pylint: disable=E0611
from PyQt5.QtWidgets import QMainWindow  # pylint: disable=E0611

from admin_view import create_admin_view


def process_cl_args():
    """
    Parsing the command line options
    :returns: A dict with the known options and an dict with the unknown
              options
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug_server', action='store_true')
    return parser.parse_known_args()


def main():
    """
    Starts the qt gui application
    :return:
    """
    args, _ = process_cl_args()
    app = QApplication([])
    win = QMainWindow(None)
    create_admin_view(win, use_debug_server=args.debug_server)
    win.show()
    app.exec_()


if __name__ == '__main__':
    main()
