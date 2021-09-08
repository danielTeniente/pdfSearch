import os
import glob
import PyPDF2
import sys


#imprime el progreso de un proceso
def drawProgressBar(percent, barLen = 20):
    sys.stdout.write("\r")
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "="
        else:
            progress += " "
    sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
    sys.stdout.flush()

#conseguir el nombre de las carpetas
def get_dirs(path='.'):
    #consigue el nombre de todos los archivos
    all_files = os.listdir(path)
    #se ubican sólo las carpetas
    ls_dir = [name for name in all_files 
        if os.path.isdir(os.path.join(path,name))]
    return ls_dir

#conseguir los nombres de los archivos PDF
def get_PDFs(path='.'):
    ls_pdfs = glob.glob(os.path.join(path,"*.pdf"))
    ls_pdfs = list(map(lambda x: str(x).replace('\\','/'),ls_pdfs))
    return ls_pdfs

#consigue el número de páginas de un PDF
def get_PDF_numPages(path='./test.pdf'):
    pdfFile = open(path,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    return pdfReader.numPages

#leer el contenido de una página archivo PDF
def get_PDF_content(path='./test.pdf',page=0):
    content = ''
    pdfFile = open(path,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    num_pages = pdfReader.numPages
    if(0<=page<num_pages):
        content+=pdfReader.getPage(page).extractText()
    content = content.strip().replace('\n\n','\n')
    pdfFile.close()
    return content

#recibe un string y lo agrega a un archivo de texto
def write_text(content='',path='.',name='book_references.txt'):
    # os.path.isfile('C:\\Windows\\System32')
    file_path = os.path.join(path,name)
    try:
        with open(file_path,'a',encoding='utf-8') as f: 
            f.write(content)
            f.write('\n\n\n')
            f.close()
        return True
    except Exception as e:
        print(e)
        return False

#busca y devuelve párrafos donde se encuentra la frase clave
def get_paragraph(phrase='',text=''):
    paragraph = ''
    phrase = str(phrase).lower()
    text = str(text).lower()

    #split por palabra buscada
    resultados = text.split(phrase)
    num_resultados = len(resultados)
    if(num_resultados>1):
        for i in range(num_resultados):
            add_char = 70
            if(i!=0):
                paragraph+=phrase.upper()
                paragraph+=resultados[i][:add_char]
                add_char=len(resultados[i])-add_char
                if(add_char<1):
                    add_char=0
                #else:
                    #add_char=min(50,add_char)
            if(i!=num_resultados-1):
                paragraph+=resultados[i][-add_char:]
    return paragraph

#escanea un libro completo
def scan_book(path,phrase):
    #conseguir el número de páginas
    num_pages = get_PDF_numPages(path)
    #info para el usuario
    #print('Libro:',path)
    #print('Extrayendo texto...')
    #esta variable tendrá el texto de cada página
    book_content = ''
    #verifica si se generó un txt
    info =''
    for page in range(num_pages):
        current_page = page+1
        drawProgressBar(percent=current_page/num_pages)
        #drawProgressBar(percent=current_page/num_pages)
        book_content = get_PDF_content(path,page)
        match = get_paragraph(phrase,text=book_content)
        if(match):
            info += 'Página '+str(current_page)+'\n'
            info += '...'+match+'...\n\n'
    #print()
    return info
    

