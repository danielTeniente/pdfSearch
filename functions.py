import os
import glob

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

