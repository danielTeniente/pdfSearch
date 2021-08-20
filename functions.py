import os
import glob
import PyPDF2

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

#leer el contenido de un archivo PDF
def get_PDF_content(path='./test.pdf',page=0):
    content = ''
    pdfFile = open(path,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    num_pages = pdfReader.numPages
    if(0<=page<num_pages):
        content+=pdfReader.getPage(page).extractText()
    content = content.strip().replace('\n',' ')
    pdfFile.close()
    return content

#recibe un string y lo agrega a un archivo de texto
def write_text(content='',path='.',name='book_references.txt'):
    # os.path.isfile('C:\\Windows\\System32')
    file_path = os.path.join(path,name)
    try:
        if(os.path.exists(file_path)):
            book_text = open(file_path,'a') 
        else:
            book_text = open(file_path,'w')
        book_text.write(content+'\n')
        book_text.close()
        return True
    except Exception as e:
        print(e)
        return False





