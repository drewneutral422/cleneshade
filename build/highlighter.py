import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QApplication
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from pygments import lexers, util
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name

class PygmentsHighlighter(QSyntaxHighlighter):
    def __init__(self, parent, style_name='monokai'):
        super().__init__(parent)
        self.formatter = []
        # Get the style (defaulting to Monokai for that dark dev look)
        self.style = get_style_by_name(style_name)
        
        # Mapping Pygments tokens to QTextCharFormat
        for token, style_values in self.style:
            _format = QTextCharFormat()
            if style_values['color']:
                _format.setForeground(QColor(f"#{style_values['color']}"))
            if style_values['bold']:
                _format.setFontWeight(QFont.Bold)
            if style_values['italic']:
                _format.setFontItalic(True)
            self.formatter.append((token, _format))

    def highlightBlock(self, text):
        # Using the Python lexer as a base (works well for Cleneshade/Iexxu)
        lexer = get_lexer_by_name('python')
        tokens = lexer.get_tokens(text)
        
        index = 0
        for token, value in tokens:
            length = len(value)
            for ttype, _format in self.formatter:
                if token in ttype:
                    self.setFormat(index, length, _format)
                    break
            index += length

class CodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cleneshade Editor")
        self.resize(800, 600)
        
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 12))
        self.editor.setStyleSheet("background-color: #272822; color: #f8f8f2;")
        
        # Attach the highlighter
        self.highlighter = PygmentsHighlighter(self.editor.document())
        self.setCentralWidget(self.editor)

def launch():
    app = QApplication(sys.argv)
    window = CodeEditor()
    window.show()
    sys.exit(app.exec_())