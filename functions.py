from genericpath import isdir
import os
from posixpath import join

#conseguir el nombre de las carpetas
def get_dirs(path='.'):
    #consigue el nombre de todos los archivos
    all_files = os.listdir(path)
    #se ubican sólo las carpetas
    ls_dir = [name for name in all_files 
        if os.path.isdir(os.path.join(path,name))]
    return ls_dir



