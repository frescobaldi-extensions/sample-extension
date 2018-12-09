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

# Sample Extensions - Action collection
#
# This file demonstrates the implementation of an action collection,
# which is used to create a consistent interface for the functionality
# (labels, icons, state)

# While it is theoretically possible to do without,
# most extensions will make heavy use of QActions
from PyQt5.QtWidgets import QAction

# Mandatory import
import extensions.actions

import icons

class SampleActions(extensions.actions.ExtensionActionCollection):
    """An Extension module must have an 'Actions' class inherited from
    extensions.ExtensionActionCollection. This will be automatically
    instantiated in the Extension object and is accessible through
    self.action_collection().

    It is necessary to define this Actions class before the Extension
    class, either by *importing* the Actions from a module or by actually
    placing the definition before the Extension in the package file. This
    is because the reference to the Actions class is done as a class
    variable and not only in the __init__() method.

    Different from regular ActionCollection objects this does not need
    a 'name' class property."""

    def createActions(self, parent):
        """Create all actions that are available within this extension.
        Will be called automatically."""
        self.sample_action = QAction(parent)
        # Icons can be loaded from the `icons` subdirectory in an extension
        self.sample_action.setIcon(icons.get('lnr-heart'))
        self._fancy_state = self.settings().get('fancy')
        self.reverse_action = QAction(parent)

    def translateUI(self):
        """This has to be implemented to set the texts
        and optionally tooltips."""
        self.sample_action.setText(_("Sample action (show message)"))
        self.sample_action.setToolTip(_("Only triggers a message box."))
        self.reverse_action.setText(_("Reverse selected text"))
        self.reverse_action.setToolTip(_("This action depends on the presence "
            + "of a selection in the editor."))

    def configure_menu_actions(self):
        """Specify the behaviour of the menus.
        If this method is not overridden the default is to use all actions
        (sorted by display name) in the Tools menu and don't produce any
        context menus.
        NOTE: It is *not* necessary to configure all three action lists,
        this is done only for demonstration purposes. Any action list that
        is *not* configured here keeps the default behaviour.
        """
        # This simply specifies a custom order for the Tools menu.
        self.set_menu_action_list('tools', [
            self.sample_action,
            self.reverse_action])

        # In the context menu of the editor we only want to have the
        # action to reverse the selected text
        self.set_menu_action_list('editor', [self.reverse_action])

        # The context menu for the Music View will show the sample action
        self.set_menu_action_list('musicview', [self.sample_action])

        # Show an action in the manuscript viewer's context menu
        self.set_menu_action_list('manuscriptview', [self.sample_action])

    # Custom functionality
    def fancy_state(self):
        return 'checked' if self._fancy_state else 'unchecked'

    def set_fancy_state(self, state):
        self._fancy_state = state
