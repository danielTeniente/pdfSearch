import re
import os
import sys
import glob
import cv2
import pdf2image
import PyPDF2
import pytesseract
from shutil import Error

# Imprime el progreso de un proceso
def drawProgressBar(percent, barLen=20):
    sys.stdout.write("\r")
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "="
        else:
            progress += " "
    sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
    sys.stdout.flush()

# Consigue el nombre de las carpetas
def get_dirs(path='.'):
    all_files = os.listdir(path)
    ls_dir = [name for name in all_files if os.path.isdir(os.path.join(path, name))]
    return ls_dir

# Consigue los nombres de los archivos PDF
def get_PDFs(path='.'):
    ls_pdfs = glob.glob(os.path.join(path, "*.pdf"))
    ls_pdfs = list(map(lambda x: str(x).replace('\\', '/'), ls_pdfs))
    return ls_pdfs

# Consigue el número de páginas de un PDF
def get_PDF_numPages(path='./test.pdf'):
    pdfFile = open(path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    num_pages = pdfReader.numPages
    pdfFile.close()
    return num_pages

def get_book_name(book_path: str) -> str:
    """Recibe el path de un libro y retorna su nombre sin la terminación .pdf"""
    if ('/' in book_path) or ('\\' in book_path):
        book_name = book_path.split('/')[-1]
        book_name = book_name.split('\\')[-1]
    else:
        book_name = book_path
    book_name = book_name.replace('.pdf', '')
    return book_name

def sanitize_name(name: str) -> str:
    """Elimina caracteres especiales y espacios, dejando solo letras y números."""
    return re.sub(r'[^a-zA-Z0-9]', '', name)

# Verifica si las imágenes ya existen
def there_are_imgs(book_path: str) -> bool:
    book_img_name = get_book_name(book_path)
    book_img_name += '_page_1.jpg'
    imgs_folder = 'book_imgs/'
    return os.path.isfile(os.path.join(imgs_folder, book_img_name))

# Genera las imágenes del libro
def create_book_images(book_path: str) -> bool:
    try:
        pages = pdf2image.convert_from_path(pdf_path=book_path, dpi=350)
        book_img_name = get_book_name(book_path)
        imgs_folder = 'book_imgs/'
        num_pages = get_PDF_numPages(book_path)
        for i, page in enumerate(pages):
            current_page = i + 1
            drawProgressBar(percent=current_page / num_pages)
            book_img_path = os.path.join(imgs_folder, f"{book_img_name}_page_{current_page}.jpg")
            page.save(book_img_path, "JPEG")
        return True
    except Error:
        print(Error)
        return False

# Separa la página en párrafos
def mark_region(image_path: str):
    im = cv2.imread(image_path)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 30)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    if len(cnts) < 1:
        return []
    line_items_coordinates = []
    last_y = cv2.boundingRect(cnts[0])[1]
    for i, c in enumerate(cnts):
        x, y, w, h = cv2.boundingRect(c)
        if ((y - last_y) ** 2 < 25 and i > 0):
            last_c = line_items_coordinates[-1]
            lx = last_c[0][0]
            line_items_coordinates[-1] = [(lx, y), (x + w, y + h)]
        else:
            line_items_coordinates.append([(x, y), (x + w, y + h)])
        last_y = y
    return line_items_coordinates

# Realiza OCR sobre una imagen y retorna el texto
def ocr_img(img_path: str) -> str:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    paragraphs = mark_region(img_path)
    image = cv2.imread(img_path)
    text = ''
    for pi in paragraphs:
        upleft_corner = pi[0]
        downright_corner = pi[1]
        img = image[upleft_corner[1]:downright_corner[1],
                    upleft_corner[0]:downright_corner[0]]
        if 0 not in img.shape:
            ret, thresh1 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
            text += str(pytesseract.image_to_string(thresh1, config='--psm 6'))
    return text

# Extrae el contenido de una página de un PDF
def get_PDF_content(path='./test.pdf', page=0):
    content = ''
    pdfFile = open(path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    num_pages = pdfReader.numPages
    if 0 <= page < num_pages:
        content += pdfReader.getPage(page).extractText()
    content = content.strip().replace('\n\n', '\n')
    pdfFile.close()
    return content

def has_selectable_text(path: str) -> bool:
    try:
        text = get_PDF_content(path, 0)
        return bool(text and text.strip())
    except Exception as e:
        return False

def write_text(content='', path='.', name='book_references.txt'):
    file_path = os.path.join(path, name)
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)
            f.write('\n\n\n')
        return True
    except Exception as e:
        print(e)
        return False

# Busca y devuelve párrafos donde se encuentra la frase clave
def get_paragraph(phrase='', text=''):
    paragraph = ''
    phrase = str(phrase).lower()
    text = str(text).lower()
    resultados = text.split(phrase)
    num_resultados = len(resultados)
    if num_resultados > 1:
        for i in range(num_resultados):
            add_char = 100
            if i != 0:
                paragraph += phrase.upper()
                paragraph += resultados[i][:add_char]
                add_char = len(resultados[i]) - add_char
                if add_char < 1:
                    add_char = 0
            if i != num_resultados - 1:
                paragraph += resultados[i][-add_char:]
    return paragraph

# Escanea el libro completo con OCR y guarda el texto en archivos organizados por libro
def scan_book_with_OCR(path: str, phrase: str):
    num_pages = get_PDF_numPages(path)
    book_name = get_book_name(path)
    sanitized_book_name = sanitize_name(book_name)
    
    base_txt_folder = 'book_txt'
    book_txt_folder = os.path.join(base_txt_folder, sanitized_book_name)
    
    if not os.path.exists(base_txt_folder):
        os.makedirs(base_txt_folder)
    
    # Verifica si el libro ya fue escaneado previamente
    if not os.path.exists(book_txt_folder):
        os.makedirs(book_txt_folder)
        
        if not there_are_imgs(path):
            print('Se crearán imágenes del libro...')
            if create_book_images(path):
                print('El libro se escaneó por primera vez y se generó una imagen por página')
            else:
                return 'El buscador inteligente tuvo problemas con este libro'
        
        imgs_folder = 'book_imgs'
        for page in range(num_pages):
            current_page = page + 1
            drawProgressBar(percent=current_page / num_pages)
            image_file = os.path.join(imgs_folder, f"{book_name}_page_{current_page}.jpg")
            txt_file = os.path.join(book_txt_folder, f"{book_name}_page_{current_page}.txt")
            
            book_content = ocr_img(image_file)
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(book_content)
            os.remove(image_file)
    else:
        print("El libro ya ha sido escaneado previamente. Usando textos cacheados.")
    
    info = ''
    for page in range(num_pages):
        current_page = page + 1
        txt_file = os.path.join(book_txt_folder, f"{book_name}_page_{current_page}.txt")
        if os.path.exists(txt_file):
            with open(txt_file, 'r', encoding='utf-8') as f:
                book_content = f.read()
        else:
            book_content = ""
        match = get_paragraph(phrase, text=book_content)
        if match:
            info += 'Página ' + str(current_page) + '\n'
            info += '...' + match + '...\n\n'
    return info

# Escanea un libro completo sin OCR, usando texto seleccionable
def scan_book(path, phrase):
    num_pages = get_PDF_numPages(path)
    info = ''
    for page in range(num_pages):
        current_page = page + 1
        drawProgressBar(percent=current_page / num_pages)
        book_content = get_PDF_content(path, page)
        match = get_paragraph(phrase, text=book_content)
        if match:
            info += 'Página ' + str(current_page) + '\n'
            info += '...' + match + '...\n\n'
    return info
