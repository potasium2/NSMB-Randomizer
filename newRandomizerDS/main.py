import sys
import random
import struct

import ndspy.rom

from PySide6 import QtCore, QtWidgets, QtGui
from level import LevelRandomizer

def main():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow(app)
    window.show()
    
    sys.exit(app.exec())

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("New Super Mario Bros. DS Randomizer")
        self.setWindowIcon(QtGui.QIcon(".\\files\\nsmbdsrando.ico"))
        
        self.parent = parent
        
        # self.ImportRom(False)
        self.InitUI()
        
    def ImportRom(self, repeat = True):
        if not repeat:
            QtWidgets.QMessageBox.information(
                self,
                self.tr("Import"),
                self.tr("Import your North American ROM of New Super Mario Bros. DS"),
            )
        
        while True:
            path, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(
                parent = self,
                caption = self.tr("Import Rom"),
                filter = "NDS ROMs (*.nds);;All Files (*)",
            )
            
            if path == '':
                if repeat:
                    return
                else:
                    sys.exit(1)
                    
            try:
                rom = ndspy.rom.NintendoDSRom.fromFile(path)
            except struct.error:
                QtWidgets.QMessageBox.warning(
                    self,
                    self.tr("Okay"),
                    self.tr("Invalid Rom File"),
                )
                continue
                
            
            if rom.name == b'NEW MARIO' and rom.idCode[3] == ord("E"):
                self.rom = rom
                self.path = path
                self.newPath = self.path
                if repeat:
                    self.InitUI()
                break
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    self.tr("Okay"),
                    self.tr("Invalid Rom File"),
                )

    def InitUI(self):
        menuBar = self.menuBar()
        menuBarFile = menuBar.addMenu(self.tr("&File"))
        menuBarFile.addAction(
            self.tr("&Import"),
            QtGui.QKeySequence.StandardKey.Open,
            self.ImportRom,
        )
        
        menuBarFile.addSeparator()
        menuBarFile.addAction(
            self.tr("&Quit"),
            QtGui.QKeySequence.StandardKey.Quit,
            QtWidgets.QApplication.quit
        )
        
        # Main Menu
        mainMenu = QtWidgets.QWidget()
        mainMenuLayout = QtWidgets.QGridLayout(mainMenu)
        
        self.mainTabs = QtWidgets.QTabWidget()
        self.mainTabs.setUsesScrollButtons(False)
        
        self.mainTabs.addTab(mainMenu, QtGui.QIcon(str('files/nsmbdsrando.ico')), self.tr("Randomize"))
        
        self.setCentralWidget(self.mainTabs)
        
        self.randomizeButton = QtWidgets.QPushButton(self.tr("Randomize"))
        self.randomizeButton.clicked.connect(self.Randomize)
        mainMenuLayout.addWidget(self.randomizeButton, 9, 0, 1, 3)
        
        # Settings
        settings = QtWidgets.QWidget()
        settingsLayout = QtWidgets.QGridLayout(settings)
        settingsLayout.setContentsMargins(0, 0, 0, 0)
        mainMenuLayout.addWidget(settings, 1, 0, 1, 1)
        
        self.customSeedCheck = QtWidgets.QCheckBox()
        self.customSeedCheck.checkStateChanged.connect(self.customSeedEnabled)
        settingsLayout.addWidget(self.customSeedCheck, 1, 1, alignment = QtCore.Qt.AlignmentFlag.AlignRight)
        seedString = QtWidgets.QLabel(self.tr("Use Custom Seed"))
        settingsLayout.addWidget(seedString, 1, 0)
        seedString.setBuddy(self.customSeedCheck)
        
        self.customSeed = QtWidgets.QLineEdit()
        settingsLayout.addWidget(self.customSeed, 2, 1, alignment = QtCore.Qt.AlignmentFlag.AlignRight)
        seedString = QtWidgets.QLabel(self.tr("Seed: "))
        settingsLayout.addWidget(seedString, 2, 0)
        seedString.setBuddy(self.customSeed)
    
    def customSeedEnabled(self, value):
        self.customSeed.setEnabled(value == QtCore.Qt.CheckState.Checked)
        if value == QtCore.Qt.CheckState.Checked:
            self.customSeed.setText(str(random.randint(0, 0xFFFFFFFF)))
        else:
            self.customSeed.setText(self.tr("i like men"))
    
    def Randomize(self):
        self.newPath, selectedFilter = QtWidgets.QFileDialog.getSaveFileName(
            parent = self,
            caption = "Save ROM",
            dir = self.newPath,
            filter = "NDS ROMs (*.nds);;All Files (*)"
        )
        
        if self.newPath == "":
            return
        
        self.thread = QtCore.QThread()
        self.randomizer = Randomizer(self)
        self.randomizer.moveToThread(self.thread)
        self.thread.started.connect(self.randomizer.run)
        self.thread.start()
        self.randomizeButton.setEnabled(False)
        
class Randomizer(QtCore.QObject):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
    def run(self):
        if self.parent.customSeedCheck.isChecked():
            seed = self.parent.customSeed.text()
        else:
            seed = str(random.randint(0, 0xFFFFFFFF))
            
        self.rom = ndspy.rom.NintendoDSRom.fromFile(self.parent.path)
        
        LevelRandomizer(self, seed, self.rom)
        self.rom.saveToFile(self.parent.newPath)
        
        
main()