from functools import partial
import sys
from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

class PyCalcGui(QMainWindow):
    """Pycalc's View (GUI)"""
    def __init__(self: QMainWindow) -> None:
        """Initialise the main view of the GUI with all properties set."""
        super().__init__()
        self.setWindowTitle('PyCalc')
        self.setFixedSize(235, 235)
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createDisplay()
        self._createButtons()
    

    def _createDisplay(self: QMainWindow) -> None:
        """Create display, set properties and add to general layout."""
        self.display = QLineEdit()
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    
    def _createButtons(self: QMainWindow) -> None:
        """Create buttons from a dict of values and positions to add to grid."""
        self.buttons = {}
        buttonsLayout = QGridLayout()
        buttons = {'7': (0, 0),
                   '8': (0, 1),
                   '9': (0, 2),
                   '/': (0, 3),
                   'C': (0, 4),
                   '4': (1, 0),
                   '5': (1, 1),
                   '6': (1, 2),
                   '*': (1, 3),
                   '(': (1, 4),
                   '1': (2, 0),
                   '2': (2, 1),
                   '3': (2, 2),
                   '-': (2, 3),
                   ')': (2, 4),
                   '0': (3, 0),
                   '00': (3, 1),
                   '.': (3, 2),
                   '+': (3, 3),
                   '=': (3, 4),
                   }
        
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(40, 40)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        
        self.generalLayout.addLayout(buttonsLayout)


    def setDisplayText(self: QMainWindow, text: str) -> None:
        """set display's text.
        
        Args:
            text (str): String of text to be added to the display."""
        self.display.setText(text)
        self.display.setFocus()
    

    def displayText(self: QMainWindow) -> str:
        """Return display text as string."""
        return self.display.text()
    

    def clearDisplay(self: QMainWindow) -> None:
        """Clear the display."""
        self.setDisplayText('')


class PyCalcCtrl:
    """PyCalc Controller class."""
    def __init__(self: object, model: Callable, view: QMainWindow) -> None:
        """Controller initializer."""
        self._evaluate = model
        self._view = view
        # Connect signals and slots
        self._connectSignals()
    

    def _calculateResult(self: object) -> None:
        """Evaluate the expression."""
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self: object, sub_exp: str)-> None:
        """Build expression."""
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        
        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)

    def _connectSignals(self: object) -> None:
        """Connect signals and slots."""
        for btnText, btn in self._view.buttons.items():
            if btnText not in {'=', 'C'}:
                btn.clicked.connect(partial(self._buildExpression, btnText))

        self._view.buttons['='].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttons['C'].clicked.connect(self._view.clearDisplay)


ERROR_MSG = "ERROR"

def evaluateExpression(expression: str) -> str:
    """Return a string of the evaluated expression.
    
    The functions serves as the model in the MVC architecture.
    
    Args:
        expression (str): Expression to be evaluated from PyCalc view
    
    Returns:
        Result (str): The result of evaluating the expression."""
    try:
        result = str(eval(expression, {}, {}))
    
    except Exception:
        result = ERROR_MSG
    
    return result


# Client code
def main() -> None:
    """Combine the Model, View and controller into an app and run it."""
    pycalc = QApplication(sys.argv)
    view = PyCalcGui()
    view.show()
    model = evaluateExpression
    PyCalcCtrl(model=model, view=view)
    sys.exit(pycalc.exec_())


if __name__ == '__main__':
    main()