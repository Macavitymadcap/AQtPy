import os
import re
import sys
from typing import Callable

from PyQt5.Qt import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QKeySequence
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QFontComboBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QToolBar

import qrc_resources

class PyTextGui(QMainWindow):
    """Main Window"""
    def __init__(self:QMainWindow, parent=None) -> None:
        """Initialise the main window."""
        super().__init__(parent)
        self.setWindowTitle("PyText")
        self.resize(800, 800)
        self.centralWidget = QTextEdit()
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setCurrentFont(QFont("Courier", 10))
        self.centralWidget.setFocus()
        self._createActions()
        self._createMenuBar()
        self._createToolBars()
        self._createStatusBar()


    def _createMenuBar(self: QMainWindow) -> None:
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

        editMenu = menuBar.addMenu("&Edit")
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)

        helpMenu = menuBar.addMenu(QIcon(":help-content.svg"), "&Help")
        helpMenu.addAction(self.helpAction)
        helpMenu.addAction(self.aboutAction)
    

    def _createToolBars(self: QMainWindow) -> None:
        """Create and add toolbars to main window."""
        self.fileToolBar =QToolBar(self)
        self.addToolBar(Qt.LeftToolBarArea, self.fileToolBar)
        self.fileToolBar.addAction(self.newAction)
        self.fileToolBar.addAction(self.openAction)
        self.fileToolBar.addAction(self.saveAction)

        self.editToolBar = QToolBar()
        self.addToolBar(Qt.RightToolBarArea, self.editToolBar)
        self.editToolBar.setAllowedAreas(Qt.LeftToolBarArea)
        self.editToolBar.addAction(self.copyAction)
        self.editToolBar.addAction(self.pasteAction)
        self.editToolBar.addAction(self.cutAction)

        displayToolBar = self.addToolBar("Display")
        self.fontComboBox = QFontComboBox(self)
        self.fontComboBox.setFocusPolicy(Qt.NoFocus)
        self.fontComboBox.setCurrentFont(QFont("Courier", 10))
        fontTip = "Change font of selected text"
        self.fontComboBox.setStatusTip(fontTip)
        displayToolBar.addWidget(self.fontComboBox)
        self.fontSizeSpinBox = QSpinBox(self)
        self.fontSizeSpinBox.setFocusPolicy(Qt.NoFocus)
        self.fontSizeSpinBox.setValue(10)
        fontSizeTip = "Change size of selected text"
        self.fontSizeSpinBox.setStatusTip(fontSizeTip)
        displayToolBar.addWidget(self.fontSizeSpinBox)
        displayToolBar.addAction(self.textColourAction)
        displayToolBar.addAction(self.textHighlightAction)
        displayToolBar.addAction(self.textFillAction)
        displayToolBar.addAction(self.textLeftAction)
        displayToolBar.addAction(self.textCentreAction)
        displayToolBar.addAction(self.textRightAction)
        displayToolBar.addAction(self.textBoldAction)
        displayToolBar.addAction(self.textItalicAction)
        displayToolBar.addAction(self.textUnderlineAction)
    

    def _createActions(self: QMainWindow) -> None:
        """Create actions using short constructor."""
        self.newAction = QAction(QIcon(":file-new.svg"), "&New", self)
        self.newAction.setShortcut(QKeySequence.New)
        newTip = "Create a new file"
        self.newAction.setStatusTip(newTip)
        self.newAction.setToolTip(newTip)

        self.openAction = QAction(QIcon(":file-open.svg"), "&Open...", self)
        self.openAction.setShortcut(QKeySequence.Open)
        openTip = "Open a existing file"
        self.openAction.setStatusTip(openTip)
        self.openAction.setToolTip(openTip)

        self.saveAction = QAction(QIcon(":file-save.svg"), "&Save", self)
        self.saveAction.setShortcut(QKeySequence.Save)
        saveTip = "Save current file"
        self.saveAction.setStatusTip(saveTip)
        self.saveAction.setToolTip(saveTip)

        self.exitAction = QAction(QIcon(":file-exit.svg"), "&Exit", self)
        exitTip = "Exit PyText"
        self.exitAction.setStatusTip(exitTip)

        self.copyAction = QAction(QIcon(":edit-copy.svg"), "&Copy", self)
        self.copyAction.setShortcut(QKeySequence.Copy)
        copyTip = "Copy selected text"
        self.copyAction.setStatusTip(copyTip)
        self.copyAction.setToolTip(copyTip)

        self.pasteAction = QAction(QIcon(":edit-paste.svg"), "Paste", self)
        self.pasteAction.setShortcut(QKeySequence.Paste)
        pasteTip = "Paste text into file"
        self.pasteAction.setStatusTip(pasteTip)
        self.pasteAction.setToolTip(pasteTip)

        self.cutAction = QAction(QIcon(":edit-cut.svg"), "Cut", self)
        self.cutAction.setShortcut(QKeySequence.Cut)
        cutTip = "Cut selected text"
        self.cutAction.setStatusTip(cutTip)
        self.cutAction.setToolTip(cutTip)

        self.helpAction = QAction("&Help", self)
        helpTip = "Help using PyText"
        self.helpAction.setStatusTip(helpTip)

        self.aboutAction = QAction("&About", self)
        aboutTip = "About PyText"
        self.aboutAction.setStatusTip(aboutTip)

        self.textColourAction = QAction(QIcon(":text-colour.svg"), "Text Colour")
        textColourTip = "Change colour of selected text"
        self.textColourAction.setStatusTip(textColourTip)

        self.textHighlightAction = QAction(QIcon(":text-highlight.svg"), "Text Highlight")
        textHighlightTip = "Highlight selected text with a colour"
        self.textHighlightAction.setStatusTip(textHighlightTip)

        self.textFillAction = QAction(QIcon(":text-fill.svg"), "Text Fill")
        textFillTip = "Set the colour of the page"
        self.textFillAction.setStatusTip(textFillTip)

        self.textLeftAction = QAction(QIcon(":text-left.svg"), "Text Left")
        textLeftTip = "Align the current paragraph to the left"
        self.textLeftAction.setStatusTip(textLeftTip)

        self.textCentreAction = QAction(QIcon(":text-centre.svg"), "Text Centre")
        textCentreTip = "Centre the current paragraph"
        self.textCentreAction.setStatusTip(textCentreTip)

        self.textRightAction = QAction(QIcon(":text-right.svg"), "Text Right")
        textRightTip = "Align the current paragraph to the right"
        self.textRightAction.setStatusTip(textRightTip)

        self.textBoldAction = QAction(QIcon(":text-bold.svg"), "Text Bold")
        self.textBoldAction.setShortcut(QKeySequence.Bold)
        textBoldTip = "Change the selected text to bold"
        self.textBoldAction.setStatusTip(textBoldTip)

        self.textItalicAction = QAction(QIcon(":text-italic.svg"), "Text Italic")
        self.textItalicAction.setShortcut(QKeySequence.Italic)
        textItalicTip = "Change the selected text to italic"
        self.textItalicAction.setStatusTip(textItalicTip)
    
        self.textUnderlineAction = QAction(QIcon(":text-underline.svg"), "Text Underline")
        self.textUnderlineAction.setShortcut(QKeySequence.Underline)
        textUnderlineTip = "Underline the selected text"
        self.textUnderlineAction.setStatusTip(textUnderlineTip)


    def _createStatusBar(self: QMainWindow) -> None:
        self.statusBar = self.statusBar()
        self.statusBar.showMessage("Ready", 3000)
        self.wcLabel = QLabel(f"Word Count: 0")
        self.statusBar.addPermanentWidget(self.wcLabel)


    def contextMenuEvent(self: object, event: object) -> None:
        """Create menu object, populate with actions and launch context menu."""
        menu = QMenu(self.centralWidget)
        menu.addAction(self.newAction)
        menu.addAction(self.openAction)
        menu.addAction(self.saveAction)
        seperator = QAction(self)
        seperator.setSeparator(True)
        menu.addAction(seperator)
        menu.addAction(self.copyAction)
        menu.addAction(self.pasteAction)
        menu.addAction(self.cutAction)
        menu.exec(event.globalPos())
    

    def closeEvent(self: object, event: object) -> None:
        """Prompt to save current file then exit program."""
        saveFile = QMessageBox.warning(
            self, "Save", "Save current file?", 
            QMessageBox.Save | QMessageBox.Close, QMessageBox.Close
        )
        if saveFile == QMessageBox.Save:
            self.saveFile()
            event.accept()
            self.close()
        
        self.close()
        

    def newFile(self: object) -> None:
        """Prompt user to save current file then set central widget as blank."""
        saveFile = QMessageBox.warning(
            self, "Save", "Save current file?", 
            QMessageBox.Save | QMessageBox.No, QMessageBox.No
        )
        if saveFile == QMessageBox.Save:
            self.saveFile()

        self.centralWidget.setText("")


    def openFile(self: object) -> None:
        """Prompt to save current file then select file to open."""
        saveFile = QMessageBox.warning(
            self, "Save", "Save current file?", 
            QMessageBox.Save | QMessageBox.No, QMessageBox.No
        )
        if saveFile == QMessageBox.Save:
            self.saveFile()

        openFileDialog = QFileDialog.getOpenFileName(
            self, "Open File", os.getenv("HOME"), 
            "All Files (*);; Text Files (*.txt);; Rich Text Files (*.rtf);; Documents (*.doc);; DocX (*.docx);; GoogleDoc (*.gdoc);; LibreOffice Doc (*.odf);; HTML (*.html);; MarkDown (*.md);; Python (*.py);; JavaScript (*.js);; Cascading Stylesheets (*.css)"
        )
        with open(openFileDialog[0], "r") as file:
            text = file.read()
            self.centralWidget.setText(text)

        fileNameRegEx = r'\b\w+.\w+\b'
        filename = re.findall(fileNameRegEx, openFileDialog[0])[0]
        self.setWindowTitle(f"PyText - {filename}")
        self.statusBar.showMessage(f"Opened {openFileDialog}", 3000)


    def saveFile(self: object) -> None:
        """Save contents of centralWidget as a file."""
        try:
            saveFileDialog = QFileDialog.getSaveFileName(
                self, "Save File", os.getenv("HOME"), 
                "All Files (*);; Text Files (*.txt);; Rich Text Files (*.rtf);; Documents (*.doc);; DocX (*.docx);; GoogleDoc (*.gdoc);; LibreOffice Doc (*.odf);; HTML (*.html);; MarkDown (*.md);; Python (*.py);; JavaScript (*.js);; Cascading Stylesheets (*.css)"
            )
            with open(saveFileDialog[0], "w") as file:
                text = self.centralWidget.toHtml()
                file.write(text)
                
            fileNameRegEx = r'\b\w+.\w+\b'
            filename = re.findall(fileNameRegEx, saveFileDialog[0])[0]
            self.setWindowTitle(f"PyText - {filename}")
            self.statusBar.showMessage(f"File saved", 3000)

        except FileNotFoundError:
            pass


    def help(self: object) -> None:
        """Logic for launching help goes here..."""
        pass


    def about(self: object) -> None:
        """Logic for showing an about dialog content goes here..."""
        with open('.\\resources\\about.txt') as file:
            about_text = file.read()
            QMessageBox.about(self, "About PyText", about_text)


    def fontColour(self: object) -> None:
        """Select font colour."""
        colourDialog = QColorDialog(self)
        self.centralWidget.setTextColor(colourDialog.getColor())


    def highlightColour(self: object) -> None:
        """Select font highlight colour."""
        colourDialog = QColorDialog(self)
        self.centralWidget.setTextBackgroundColor(colourDialog.getColor())


    def fillColour(self: object) -> None:
        """Select page background colour."""
        colourDialog = QColorDialog(self)
        rgb = colourDialog.getColor().getRgb()
        self.centralWidget.setStyleSheet(f"background: rgb({rgb[0]}, {rgb[1]}, {rgb[2]})")


    def textLeft(self: object) -> None:
        """Align current paragrah left."""
        self.centralWidget.setAlignment(Qt.AlignLeft)

    
    def textCentre(self: object) -> None:
        """Centre current paragrah."""
        self.centralWidget.setAlignment(Qt.AlignHCenter)


    def textRight(self: object) -> None:
        """Align current paragrah right."""
        self.centralWidget.setAlignment(Qt.AlignRight)
    

    def textBold(self: object) -> None:
        """Set selected text as bold."""
        if self.centralWidget.fontWeight() >= 51:
            self.centralWidget.setFontWeight(50)
        else:
            self.centralWidget.setFontWeight(75) 
           

    def textItalic(self: object) -> None:
        """Set selected text as italic."""
        fontCheck = self.centralWidget.textCursor().charFormat()
        if fontCheck.fontItalic():
            self.centralWidget.setFontItalic(False)
        else:
            self.centralWidget.setFontItalic(True)

    
    def textUnderline(self: object) -> None:
        """Underline the selected text."""
        fontCheck = self.centralWidget.textCursor().charFormat()
        if fontCheck.fontUnderline():
            self.centralWidget.setFontUnderline(False)
        else:
            self.centralWidget.setFontUnderline(True)


class PyTextCtrl:
    """PyText Controller class."""
    def __init__(self: object, model: object, view: QMainWindow) -> None:
        """Controller initializer."""
        self._view = view
        self._model = model
        self._connectSignals()


    def _fontAndSize(self: object) -> QFont:
        spinBox = self._view.fontSizeSpinBox
        comboBox = self._view.fontComboBox
        return self._model.getFont(comboBox, spinBox)


    def _fontSizeValue(self: object) -> int:
        spinBox = self._view.fontSizeSpinBox
        return self._model.getSize(spinBox)


    def _wordCountString(self: object) -> str:
        """Return string of current word count."""
        return f"Word Count: {self._model.getWordCount(self._view.centralWidget.toPlainText())}"


    def _connectSignals(self: object) -> None:
        """Connect signals and slots."""
        self._view.centralWidget.textChanged.connect(
            lambda: self._view.wcLabel.setText(self._wordCountString())
            )
        self._view.newAction.triggered.connect(self._view.newFile)
        self._view.openAction.triggered.connect(self._view.openFile)
        self._view.saveAction.triggered.connect(self._view.saveFile)
        self._view.exitAction.triggered.connect(self._view.closeEvent)
        self._view.copyAction.triggered.connect(self._view.centralWidget.copy)
        self._view.pasteAction.triggered.connect(self._view.centralWidget.paste)
        self._view.cutAction.triggered.connect(self._view.centralWidget.cut)
        self._view.helpAction.triggered.connect(self._view.help)
        self._view.aboutAction.triggered.connect(self._view.about)
        self._view.fontSizeSpinBox.valueChanged.connect(
            lambda: self._view.centralWidget.setFontPointSize(self._fontSizeValue())
        )
        self._view.fontComboBox.currentFontChanged.connect(
            lambda: self._view.centralWidget.setCurrentFont(self._fontAndSize())
        )
        self._view.textColourAction.triggered.connect(self._view.fontColour)
        self._view.textHighlightAction.triggered.connect(self._view.highlightColour)
        self._view.textFillAction.triggered.connect(self._view.fillColour)
        self._view.textLeftAction.triggered.connect(self._view.textLeft)
        self._view.textCentreAction.triggered.connect(self._view.textCentre)
        self._view.textRightAction.triggered.connect(self._view.textRight)
        self._view.textBoldAction.triggered.connect(self._view.textBold)
        self._view.textItalicAction.triggered.connect(self._view.textItalic)
        self._view.textUnderlineAction.triggered.connect(self._view.textUnderline)


class PyTextModl:
    """Model for running functions through view and control."""

    def getWordCount(self: object, string: str) -> int:
            """Return count of words in given string."""
            word = r'\b\w+\b'
            wordMatches = re.findall(word, string)
            return len(wordMatches)


    def getSize(self: object, spinBox: QSpinBox) -> int:
        """Return value of spinBox object as int."""
        return spinBox.value()
    

    def getFont(self: object, fontComboBox: QFontComboBox, spinBox: QSpinBox) -> QFont:
        """Return a Qfont from the values of the font combo and spin boxes."""
        size = self.getSize(spinBox)
        font = fontComboBox.currentText()
        return QFont(font, size)


def main():
    app = QApplication(sys.argv)
    view = PyTextGui()
    view.show()
    model = PyTextModl()
    PyTextCtrl(model=model, view=view)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()