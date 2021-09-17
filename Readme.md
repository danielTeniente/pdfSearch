# PDF references extractor
Este proyecto está orientado a extraer referencias bilbiográficas de archivos PDF.

## Funcionamiento
El archivo [main.py](./main.py) ejecuta una búsqueda de palabras, ingresadas por el usuario, en un conjunto de PDFs ubicados en una carpeta.

Ejemplo de ejecución:
* main.py Referencias

Donde 'Referencias' es la carpeta que tiene los
PDFs donde se buscarán las palabras clave.

## Requisitos de funcionamiento
* Poppler para el manejo de PDFs:
https://anaconda.org/conda-forge/poppler

* Tesseract para el funcionamiento del OCR:
https://github.com/UB-Mannheim/tesseract/wiki

* Se debe configurar el path de tesseract. Por defecto la configuración es: 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

## Lista de tareas
* Almacenar los archivos txt página por página de un libro ya buscado para no tener que usar el OCR una y otra vez, ahorrando tiempo.



