#!/usr/bin/env python

# -*- coding: utf-8 -*-
#
# Copyright (C) 2014-2016  Michell Stuttgart Faria

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.

# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from PySide import QtGui, QtCore
from os.path import abspath

from main_window_model import MainWindowModel
from main_window_view import MainWindowView

DATADIRS = (
        abspath('.'),
        '/usr/share/pynocchio',
        '/usr/local/share/pynocchio',
        QtCore.QDir.homePath() + '/.local/share/pynocchio',
    )

QLocale = QtCore.QLocale
QLibraryInfo = QtCore.QLibraryInfo
QTranslator = QtCore.QTranslator
QFileInfo = QtCore.QFileInfo
QFile = QtCore.QFile


class Pynocchio(QtGui.QApplication):

    def __init__(self):
        super(Pynocchio, self).__init__(sys.argv)
        self.setOrganizationName('Pynocchio')
        self.setApplicationName('Pynocchio')
        if hasattr(self, 'setApplicationDisplayName'):
            self.setApplicationDisplayName('Pynocchio')

        translator = QTranslator()

        for path in DATADIRS:
            self.addLibraryPath(path)

        for path in DATADIRS:
            if translator.load('pynocchio_' + QLocale.system().name(),
                               path + '/locale'):
                break
        qt_translator = QTranslator()
        qt_translator.load('qt_' + QLocale.system().name(),
                           QLibraryInfo.location(QLibraryInfo.TranslationsPath))
        self.installTranslator(translator)
        self.installTranslator(qt_translator)

        self.model = MainWindowModel()
        self.view = MainWindowView(self.model)

    def run(self):

        self.view.show()

        if len(sys.argv) > 1:
            file_name = QFileInfo(sys.argv[1]).canonicalFilePath()
            if QFile.exists(file_name):
                self.view.open_comics(file_name)

        sys.exit(self.exec_())
