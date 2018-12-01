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
from . import actions, config, widget

class Extension(extensions.Extension):
    """Entry point for an extension.

    An extension must export exactly one class Extension(extensions.Extension).
    It is essential to inherit from extensions.Extension and to keep the class
    name Extension. This is how the extension is loaded and validated.

    The Extension class *may* override a few methods and can implement
    arbitrary functionality. Providing a Tool Panel is optional.
    """

    # Configuration is mostly done with class variables:

    # Specify action collection class.
    # Details about this class are given in actions.py
    _action_collection_class = actions.SampleActions

    # Specify a panel widget class to trigger the creation
    # of a Tool panel. Providing the dock_area is optional.
    _panel_widget_class = widget.SampleWidget
    _panel_dock_area = Qt.LeftDockWidgetArea

    # Specify a class for a configuration widget (in the Preferences)
    _config_widget_class = config.SampleConfig


    def __init__(self, global_extensions):
        """Initialize the extension object. global_extensions
        will be referenced through self.parent()."

        The __init__ method is not strictly necessary for an
        extension. As is visible from this sample extension
        it is only used to connect the actions to their handlers.
        If an extension relies exclusively on the Tool panel
        everything can be implemented there, and the Extension
        class may be complete with setting the class variables.
        """

        super(Extension, self).__init__(global_extensions)

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
        message = _("Sample Action")
        s = extensions.ExtensionSettings()
        informative_message = (
            _("This is a message box triggered by a sample action "
              "of the sample extension.\n\n"
              "The FANCY option is {}checked.".format(
              '' if s.value('sample/fancy', False, bool) else 'un')))
        QMessageBox.information(
            self.parent().mainwindow(), message,
            informative_message, QMessageBox.Ok)

    def update_selection_actions(self, has_selection):
        """Called when the selection state of the current document changed.
        has_selection is a Boolean indicating whether the cursor now has a
        selection or not."""
        ac = self.action_collection()
        ac.reverse_action.setEnabled(has_selection)
