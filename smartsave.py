import logging

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc
import os
from pymel.core.system import Path

log = logging.getLogger(__name__)

def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)

class SmartSaveUI(QtWidgets.QDialog):
    """Smart Class UI Class"""


    def __init__(self):
        super(SmartSaveUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Smart Save")
        self.setMinimumWidth(500)
        self.setMaximumHeight(200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scenefile = SceneFile()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Smart Save")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.folder_lay = self._create_folder_ui()
        self.filename_lay = self._create_filename_ui()
        self.button_lay = self._create_buttons_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.folder_lay)
        self.main_lay.addLayout(self.filename_lay)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def create_connections(self):
        """connect signals and slots"""
        self.folder_browse_btn.clicked.connect(self._browse_folder)
        self.save_btn.clicked.connect(self._save)
        self.save_inc_btn.clicked.connect(self._save_increment)

        @QtCore.Slot()
        def _save_increment(self):
            """save an increment of the scene"""
            self._set_scenefile_properties_from_ui()
            self.scenefile.save_increment()
            self.ver_sbx.setValue(self.scenefile.ver)

        @QtCore.Slot()
        def _save(self):
            """save the scene"""
            self._set_scenefile_properties_from_ui()
            self.scenefile.save()

    def _set_scenefile_properties_from_ui(self):
        self.scenefile.folder_path = self.folder_le.text()
        self.scenefile.descriptor = self.descriptor_le.text()
        self.scenefile.task = self.task_le.text()
        self.scenefile.ver = self.ver_sbx.value()
        self.scenefile.ext = self.ext_lbl.text()

        @QtCore.Slot()
        def _browse_folder(self):
            """opens a dialogue box to browse the folder"""
            folder = QtWidgets.QFileDialog.getExistingDirectory(
                parent=self, caption="Select Folder",
                dir=self.folder_le.text(),
                options=QtWidgets.QFileDialog.ShowDirsOnly |
                        QtWidgets.QFileDialog.DontResolveSymlinks)
            self.folder_le.setText(folder)