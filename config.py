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

# The Sample extension's configuration widget

# The PyQt5 imports are for the actual widget, not for the integration
from PyQt5.QtWidgets import QCheckBox, QLabel, QVBoxLayout, QWidget

# A customized QSettings descendant has to be used to
# handle preferences storage
from extensions import ExtensionSettings

class SampleConfig(QWidget):
    """The extension's configuration widget.
    This can be any QWidget descendant but must follow several rules.
    It is automatically shown in the Preferences page.
    """
    def __init__(self, group):
        # group will become the widget's parent, so the
        # preference group can be accessed through self.parent()
        super(SampleConfig, self).__init__(group)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.label = QLabel(_(
            "Sample extension configuration.\n"
            "The setting of the following checkbox"
            "will be reflected in the message box of "
            "the sample action.\n"))
        layout.addWidget(self.label)

        # The 'toggled' signal of the checkbox is mapped to
        # the 'changed' signal of group (or self.parent()).
        # Any change in the widget must trigger the group's
        # 'changed' signal to notify Frescobaldi of the change
        # (and enable the "Apply" button).
        # An alternative solution to this is explicitly doing
        # self.parent().changed.emit() in a slot function.
        self.check_box = QCheckBox(toggled=group.changed)
        layout.addWidget(self.check_box)

        self.translateUI()

    def translateUI(self):
        self.check_box.setText(_("FANCY Preference"))

    def load_settings(self):
        """Set the GUI elements to the state from the settings.
        A configuration widget must implement loadSettings() and
        saveSettings().
        """
        # Instead of a QSettings() object an extensions.ExtensionSettings()
        # object has to be used. An extension should handle its settings
        # within a group namespace.
        s = ExtensionSettings()
        s.beginGroup('sample')
        self.check_box.setChecked(s.value('fancy', False, bool))

    def save_settings(self):
        s = ExtensionSettings()
        s.beginGroup('sample')
        s.setValue('fancy', self.check_box.isChecked())
