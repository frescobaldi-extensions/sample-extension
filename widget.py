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

# The Sample extension's widget

# The PyQt5 imports are for the example implementation,
# they are not generally needed for a panel's widget.
from PyQt5.QtWidgets import QLabel, QVBoxLayout

# The mandatory import
import extensions.widget

class SampleWidget(extensions.widget.ExtensionWidget):
    """The panel's actual widget.
    This may be any descendant of QWidget, but using extensions.ExtensionWidget
    as a base class provides a few extra convenience properties.
    """
    def __init__(self, panel):
        super(SampleWidget, self).__init__(panel)
        layout = QVBoxLayout()
        self.setLayout(layout)
        text = [_("A Simple Tool panel")]

        # direct access to self.extension()
        text.append(_('From the extension "{}"'.format(
            self.extension().display_name())))
        text.append('')
        text.append(_('The extension exposes these Actions:'))

        # direct access to self.action_collection()
        for a in self.action_collection().by_text():
            text.append('- {}'.format(a.text()))

        text.append('')
        text.append(_('The extension can access anything '))
        text.append(_('in Frescobaldi, for example the '))
        text.append(_('current document:'))
        self.label = QLabel('\n'.join(text))
        layout.addWidget(self.label)

        self.current_doc_label = QLabel()
        layout.addWidget(self.current_doc_label)
        layout.addStretch()

        # direct access to self.mainwindow() and its actions
        self.mainwindow().currentDocumentChanged.connect(self.handle_document)

    def handle_document(self):
        # direct access to self.current_document()
        # Note that this is not available yet when the extension is loaded
        # (MainWindow loads documents after menus and extension).
        doc = self.current_document()
        if doc:
            self.current_doc_label.setText(doc.documentName())
