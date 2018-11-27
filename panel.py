# This file is part of the Frescobaldi Extensions project,
# https://github.com/frescobaldi-extensions
#
# Copyright (c) 2018 by Urs Liska and others
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# See http://www.gnu.org/licenses/ for more information.

# An extension Panel


# Qt is usually needed for specifying a default docking area
from PyQt5.QtCore import Qt

import extensions.panel

class SamplePanel(extensions.panel.ExtensionPanel):
    """An extremely basic extension Tool panel.
    This must inherit from extensions.ExtensionPanel and provides the
    basic infrastructure to be added to the Tools menu and the list of
    dockable panels.

    The main tasks of this specific class is to provide strings for
    the GUI and to override createWidget to produce the actual
    widget for the panel.

    The base class provides some convenience properties to directly
    access the extension itself (self.extension()), the extension's
    action collection and the main window.
    """
    def __init__(self, extension):
        super(SamplePanel, self).__init__(extension)
        self.hide()
# TODO: How can we handle shortcuts for arbitrary extensions?
#        self.toggleViewAction().setShortcut(QKeySequence("Meta+Alt+Z"))
        self.mainwindow().addDockWidget(Qt.LeftDockWidgetArea, self)

    def translateUI(self):
        # Used as the panel's title or in tabs.
        self.setWindowTitle(_("A basic sample extension"))

    def createWidget(self):
        # Import the widget module only here. This way the module is only
        # loaded when the Tool panel is actually opened.
        from . import widget
        return widget.SampleWidget(self)
