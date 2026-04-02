import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

app = None
window = None

def init():
    global app, window
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.setWindowTitle("CleneQt Universal Engine")
    window.resize(800, 600)
    
    central = QtWidgets.QWidget()
    window.setCentralWidget(central)
    window.layout = QtWidgets.QVBoxLayout(central)

def add(widget_type, text=None):
    """
    Universal Widget Creator.
    Usage: add("QPushButton", "Click Me") or add("QLineEdit")
    """
    if not window: 
        print("Error: Init CleneQt first.")
        return

    try:
        # Dynamically get the class from QtWidgets (e.g., QtWidgets.QPushButton)
        widget_class = getattr(QtWidgets, widget_type)
        
        # Create the instance
        if text:
            new_widget = widget_class(str(text))
        else:
            new_widget = widget_class()
            
        # Add to the main layout
        window.layout.addWidget(new_widget)
        return new_widget
    except AttributeError:
        print(f"CleneQt Error: '{widget_type}' is not a valid Qt Widget.")
    except Exception as e:
        print(f"Runtime Error creating {widget_type}: {e}")

def add_dock(title, side="left"):
    if not window: return
    dock = QtWidgets.QDockWidget(str(title), window)
    sides = {
        "left": Qt.LeftDockWidgetArea, "right": Qt.RightDockWidgetArea,
        "top": Qt.TopDockWidgetArea, "bottom": Qt.BottomDockWidgetArea
    }
    window.addDockWidget(sides.get(side.lower(), Qt.LeftDockWidgetArea), dock)
    # Default internal widget for the dock
    dock.setWidget(QtWidgets.QTextEdit())

def show():
    if window:
        window.show()
        app.exec_()