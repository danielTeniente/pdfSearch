import os
import glob
import PyPDF2

def get_dirs(path='.'):
    all_files = os.listdir(path)
    ls_dir = [name for name in all_files if os.path.isdir(os.path.join(path, name))]
    return ls_dir

def get_PDFs(path='.'):
    ls_pdfs = glob.glob(os.path.join(path, "*.pdf"))
    ls_pdfs = list(map(lambda x: str(x).replace('\\', '/'), ls_pdfs))
    return ls_pdfs

def get_PDF_numPages(path='./test.pdf'):
    pdfFile = open(path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    num_pages = pdfReader.numPages
    pdfFile.close()
    return num_pages

def get_book_name(book_path: str) -> str:
    if ('/' in book_path) or ('\\' in book_path):
        book_name = book_path.split('/')[-1]
        book_name = book_name.split('\\')[-1]
    else:
        book_name = book_path
    book_name = book_name.replace('.pdf', '')
    return book_name

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

def scan_book(path, phrase):
    num_pages = get_PDF_numPages(path)
    info = ''
    for page in range(num_pages):
        current_page = page + 1
        print(f"Procesando página {current_page}/{num_pages}", end='\r')
        book_content = get_PDF_content(path, page)
        match = get_paragraph(phrase, text=book_content)
        if match:
            info += 'Página ' + str(current_page) + '\n'
            info += '...' + match + '...\n\n'
    return info
