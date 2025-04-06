import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import functions  # Se asume que este módulo contiene las funciones get_PDFs, get_dirs, scan_book y scan_book_with_OCR

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Buscador de referencias")
        self.setWindowIcon(QtGui.QIcon("./imgs/favicon.ico"))
        
        # Variable para almacenar la carpeta seleccionada
        self.dir_path = ''
        
        # Widget central y layout principal
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        
        # Título de la aplicación
        title_label = QtWidgets.QLabel("Buscador de referencias")
        title_font = QtGui.QFont()
        title_font.setPointSize(25)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Layout para el formulario de búsqueda
        form_layout = QtWidgets.QGridLayout()
        main_layout.addLayout(form_layout)
        
        # Etiqueta y campo para ingresar el término de búsqueda
        search_label = QtWidgets.QLabel("¿Qué palabras quieres buscar?")
        search_font = QtGui.QFont()
        search_font.setPointSize(15)
        search_label.setFont(search_font)
        form_layout.addWidget(search_label, 0, 0)
        
        self.search_edit = QtWidgets.QLineEdit()
        self.search_edit.setFont(search_font)
        form_layout.addWidget(self.search_edit, 0, 1)
        
        # Etiqueta y combobox para seleccionar un libro
        book_label = QtWidgets.QLabel("Selecciona un libro")
        book_label.setFont(search_font)
        form_layout.addWidget(book_label, 1, 0)
        
        self.book_combo = QtWidgets.QComboBox()
        self.book_combo.setFont(QtGui.QFont("", 12))
        form_layout.addWidget(self.book_combo, 1, 1)
        
        # Botón para seleccionar la carpeta de documentos
        folder_btn = QtWidgets.QPushButton("Seleccionar carpeta")
        folder_btn.setFont(search_font)
        folder_btn.clicked.connect(self.select_folder)
        form_layout.addWidget(folder_btn, 2, 1)
        
        # Etiqueta para los resultados
        result_label = QtWidgets.QLabel("Resultados:")
        result_label.setFont(search_font)
        main_layout.addWidget(result_label)
        
        # Área de texto para mostrar los resultados
        self.results_text = QtWidgets.QTextEdit()
        self.results_text.setFont(search_font)
        main_layout.addWidget(self.results_text)
        
        # Layout horizontal para los botones de búsqueda
        btn_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(btn_layout)
        
        search_btn = QtWidgets.QPushButton("Buscar")
        search_btn.setFont(search_font)
        search_btn.clicked.connect(self.press_search_btn)
        btn_layout.addWidget(search_btn)
        
        ocr_btn = QtWidgets.QPushButton("Búsqueda inteligente")
        ocr_btn.setFont(search_font)
        ocr_btn.clicked.connect(self.press_OCR_btn)
        btn_layout.addWidget(ocr_btn)
    
    def select_folder(self):
        """Permite al usuario seleccionar la carpeta de documentos y actualiza el combobox."""
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Selecciona la carpeta de documentos")
        if folder:
            self.dir_path = folder
            # Se obtienen los PDFs de la carpeta y de sus subcarpetas
            books_path = functions.get_PDFs(self.dir_path)
            sub_dirs = functions.get_dirs(self.dir_path)
            for sub in sub_dirs:
                folder_path = f"{self.dir_path}/{sub}"
                books_path += functions.get_PDFs(folder_path)
            # Se actualiza la lista en el combobox
            self.book_combo.clear()
            self.book_combo.addItems(books_path)
    
    def press_search_btn(self):
        """Ejecuta la búsqueda estándar en el libro seleccionado."""
        self.results_text.clear()
        selected_book = self.book_combo.currentText()
        search_text = self.search_edit.text()
        if search_text and selected_book:
            self.results_text.append(selected_book)
            print(selected_book)
            resultados = functions.scan_book(selected_book, search_text)
            content = resultados if resultados else "No se ha encontrado información."
            self.results_text.append(content)
            print()
    
    def press_OCR_btn(self):
        """Ejecuta la búsqueda inteligente (OCR) tras confirmar con el usuario."""
        self.results_text.clear()
        selected_book = self.book_combo.currentText()
        search_text = self.search_edit.text()
        if search_text and selected_book:
            reply = QtWidgets.QMessageBox.question(self, "Búsqueda inteligente",
                                                   "La búsqueda inteligente tarda más tiempo\n"
                                                   "para poder leer mejor el contenido.\n"
                                                   "¿Quiere continuar?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.results_text.append(selected_book)
                print(selected_book)
                resultados = functions.scan_book_with_OCR(selected_book, search_text)
                content = resultados if resultados else "No se ha encontrado información."
                self.results_text.append(content)
                print()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
