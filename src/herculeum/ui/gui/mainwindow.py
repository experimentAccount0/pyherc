# -*- coding: utf-8 -*-

# Copyright (c) 2010-2017 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Module for main window related functionality
"""

import PyQt4.QtGui
from herculeum.ui.controllers import EndScreenController, StartGameController
from herculeum.ui.gui.endscreen import EndScreen
from herculeum.ui.gui.eventdisplay import EventMessageDockWidget
from herculeum.ui.gui.map import PlayMapWindow
from herculeum.ui.gui.menu import MenuDialog
from herculeum.ui.gui.startgame import StartGameWidget
from PyQt4.QtCore import QFile, Qt
from PyQt4.QtGui import (QAction, QApplication, QCursor, QDialog, QIcon,
                         QMainWindow, QPixmap, QSplashScreen)


class QtUserInterface():
    """
    Class for Qt User Interface

    .. versionadded:: 0.9
    """
    def __init__(self, application):
        """
        Default constructor
        """
        super().__init__()

        self.application = application
        self.splash_screen = None

        self.qt_app = QApplication([])
        # self.qt_app.setOverrideCursor(QCursor(Qt.BlankCursor))

    def show_splash_screen(self):
        """
        Show splash screen
        """
        file = QFile(':herculeum.qss')
        file.open(QFile.ReadOnly)
        styleSheet = str(file.readAll().data(), 'ascii')
        self.qt_app.setStyleSheet(styleSheet)

        pixmap = QPixmap(':splash.png')
        self.splash_screen = QSplashScreen(pixmap)
        self.splash_screen.show()

    def show_main_window(self):
        """
        Show main window
        """
        main_window = MainWindow(self.application,
                                 self.application.surface_manager,
                                 self.qt_app,
                                 None,
                                 Qt.FramelessWindowHint,
                                 StartGameController(self.application.level_generator_factory,
                                                     self.application.creature_generator,
                                                     self.application.item_generator,
                                                     self.application.config.start_level))

        self.splash_screen.finish(main_window)
        main_window.show_new_game()

        self.qt_app.exec_()


class MainWindow(QMainWindow):
    """
    Class for displaying main window

    .. versionadded:: 0.5
    """
    def __init__(self, application, surface_manager, qt_app, parent, flags,
                 controller):
        """
        Default constructor
        """
        super().__init__(parent, flags)

        self.application = application
        self.surface_manager = surface_manager
        self.qt_app = qt_app
        self.controller = controller

        self.__set_layout()

    def __set_layout(self):

        exit_action = QAction(QIcon(':exit-game.png'),
                              '&Quit',
                              self)

        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Quit game')
        exit_action.triggered.connect(PyQt4.QtGui.qApp.quit)

        inventory_action = QAction(QIcon(':inventory.png'),
                                   'Inventory',
                                   self)
        inventory_action.setShortcut('Ctrl+I')
        inventory_action.setStatusTip('Show inventory')
        inventory_action.triggered.connect(self.__show_menu)

        character_action = QAction(QIcon(':character.png'),
                                   'Character',
                                   self)
        character_action.setShortcut('Ctrl+C')
        character_action.setStatusTip('Show character')

        self.map_window = PlayMapWindow(parent=None,
                                        model=self.application.world,
                                        surface_manager=self.surface_manager,
                                        action_factory=self.application.action_factory,
                                        rng=self.application.rng,
                                        rules_engine=self.application.rules_engine,
                                        configuration=self.application.config)
        self.setCentralWidget(self.map_window)

        self.map_window.MenuRequested.connect(self.__show_menu)
        self.map_window.EndScreenRequested.connect(self.__show_end_screen)

        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle('Herculeum')
        self.setWindowIcon(QIcon(':rune-stone.png'))
        self.showMaximized()

    def show_new_game(self):
        """
        Show new game dialog
        """
        app = self.application

        start_dialog = StartGameWidget(generator=app.player_generator,
                                       config=self.application.config.controls,
                                       parent=self,
                                       application=self.application,
                                       surface_manager=self.surface_manager,
                                       flags=Qt.Dialog | Qt.CustomizeWindowHint)

        result = start_dialog.exec_()

        if result == QDialog.Accepted:
            player = start_dialog.player_character

            intro_text = self.controller.setup_world(self.application.world,
                                                     player)

            player.register_for_updates(self.map_window.hit_points_widget)
            self.map_window.hit_points_widget.show_hit_points(player)
            self.map_window.hit_points_widget.show_spirit_points(player)
            self.map_window.message_widget.text_edit.setText(intro_text)

            self.__show_map_window()

    def __show_map_window(self):
        """
        Show map window
        """
        self.map_window.construct_scene()

    def __show_message_window(self, character):
        """
        Show message display

        :param character: character which events to display
        :type character: Character
        """
        messages_display = EventMessageDockWidget(self, character)

        self.addDockWidget(Qt.BottomDockWidgetArea,
                           messages_display)

    def __show_menu(self):
        """
        Show menu
        """
        menu_dialog = MenuDialog(self.surface_manager,
                                 self.application.world.player,
                                 self.application.action_factory,
                                 self.application.config.controls,
                                 self,
                                 Qt.Dialog | Qt.CustomizeWindowHint)
        menu_dialog.exec_()

    def __show_end_screen(self):
        """
        Show end screen

        .. versionadded:: 0.8
        """
        end_screen = EndScreen(self.application.world,
                               self.application.config.controls,
                               self,
                               Qt.Dialog | Qt.CustomizeWindowHint,
                               controller=EndScreenController())

        end_screen.exec_()
        self.qt_app.quit()
