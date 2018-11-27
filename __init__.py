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

##############################
# Sample Frescobaldi extension
##############################

# This is a minimal sample extension for use with Frescobaldi
# (http://frescobaldi.org, https://github.com/wbsoft/frescobaldi),
# intended to demonstrate the basic steps to create an extension.
#
# An extension is essentially a Python package that exports one
# specific object and adheres to a few more rules.
# The package must be located within an extensions directory that
# is known to Frescobaldi. Once it is loaded it has access to all
# packages and modules from within Frescobaldi, just like the regular
# Frescobaldi code. For convenience a number of properties (e.g.
# the current document, cursor, etc.) are directly made available as
# properties of the extension.

from PyQt5.QtCore import Qt

# This is the mandatory import from Frescobaldi, making the extension
# API available.
import extensions

# An action collection is imported from a separate module in the pacakge.
# It is mandatory that the actions class is defined before the
# Extension itself (which could be within this file, though).
from . import actions, widget

class Extension(extensions.Extension):
    """Entry point for an extension.

    An extension must export exactly one class Extension(extensions.Extension).
    It is essential to inherit from extensions.Extension and to keep the class
    name Extension. This is how the extension is loaded and validated.

    The Extension class *may* override a few methods and can implement
    arbitrary functionality. Providing a Tool Panel is optional.
    """

    # Two class variables are required for proper operation:

    # The display name is used as the title of the extension's
    # Tools menu submenu entry, and for the list in the Preferences
    # dialog.
    _display_name = "Sample Extension"

    # Specify action collection class.
    # Details about this class are given in actions.py
    _action_collection_class = actions.SampleActions

    def __init__(self, global_extensions):
        """Initialize the extension object. global_extensions
        will be referenced through self.parent()."""

        # If the extension provides a Tool Panel it must be specified
        # here (NOTE: *before* calling super()).
        # All the functionality is implemented in the panel's *widget*,
        # so passing the widget class is the main point of information,
        # additionally the (initial) dock area for the panel is specified.
        self.set_panel_properties(
            widget.SampleWidget,
            dock_area=Qt.LeftDockWidgetArea)

        super(Extension, self).__init__(global_extensions)

        # Everything up to this point is the necessary boilerplate code
        # for defining an extension. The actual *work* of the extension
        # is implemented in the action collection and the widget while
        # the remainder of this file is used to coordinate everything,
        # mostly by handling the actions.

        # The appropriate action collection is implicitly created
        ac = self.action_collection()
        # Connect the actions with handler methods
        ac.sample_action.triggered.connect(self.do_sample_action)
        ac.reverse_action.triggered.connect(self.do_reverse_action)

        # Respond to changes in the current document. We update the
        # status of (some of) our actions depending on whether there
        # is a selection or not.
        self.mainwindow().selectionStateChanged.connect(
            self.update_selection_actions)

    # The following methods implement the custom sample implementation
    # of the extension. In case of very large extensions it may be good
    # practice to forward these action slots to code in a separate module.
    def do_reverse_action(self):
        """Just a silly sample action that reverses the content
        of the current cursor's selection."""
        # self.text_cursor() gives direct acces to the current document's
        # QTextCursor instance.
        cursor = self.text_cursor()
        cursor.insertText(cursor.selectedText()[::-1])

    def do_sample_action(self):
        """Standalone action showing a message box."""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self.parent().mainwindow(), "Sample Action",
            "This is a message box triggered by a sample action "
            + "of '{}'.".format(self.display_name()), QMessageBox.Ok)

    def update_selection_actions(self, has_selection):
        """Called when the selection state of the current document changed.
        has_selection is a Boolean indicating whether the cursor now has a
        selection or not."""
        ac = self.action_collection()
        ac.reverse_action.setEnabled(has_selection)
