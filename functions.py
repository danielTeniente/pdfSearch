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
def get_PDF_content(path='./test.pdf'):
    content = ''
    pdfFile = open(path,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    num_pages = pdfReader.numPages
    for i in range(num_pages):
        content+=pdfReader.getPage(0).extractText()
    content = content.strip().replace('\n',' ')
    pdfFile.close()
    return content
