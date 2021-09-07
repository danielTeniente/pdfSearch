# imprimir el texto de un libro como AI
import functions
import time
#para colocarlo en el nombre
t = time.time()

def scan_book(path,phrase,output_name='text.txt'):
    #conseguir el número de páginas
    num_pages = functions.get_PDF_numPages(path)
    #info para el usuario
    print('Libro:',path)
    print('Extrayendo texto...')
    #esta variable tendrá el texto de cada página
    book_content = ''
    #verifica si se generó un txt
    got_txt = False
    for page in range(num_pages):
        current_page = page+1
        functions.drawProgressBar(percent=current_page/num_pages)
        book_content = functions.get_PDF_content(path,page)
        match = functions.get_paragraph(phrase,text=book_content)
        if(match):
            got_txt = True
            info = 'Página '+str(current_page)+'\n'
            info += '...'+match+'...'
            if(not functions.write_text(info,
                path='./searching',name=output_name)):
                print('Grave Error al extraer información')
    print()
    if(got_txt):
        print('Resultados encontrados y almacenados en:',output_name)

    

def main(args):
    """
    [ES]
    Uso:
    python main.py 'carpeta_de_referencias' 
    Parámetros:
    carpeta_de_referencias: dirección o nombre de la carperta
        donde se almacenan los PDFs. Si el nombre de la carpeta
        tiene espacios, debes usar '' para engolbarlo.
    Ejemplos:
    python main.py Referencias
    python main.py 'Carpeta de referencias'

    [EN]
    Use:
    python main.py 'reference_folder' 
    Parameters:
    reference_folder: path or name of the folder used to
        store PDFs. If there are spaces in folder name, you have to
        use '' to englobe it.
    Examples:
    python main.py References
    python main.py 'References folder'
    """
    if(len(args)==1):

        #path de la carpeta que será analizada
        dir_path =str(args[0])
        #lo que se va a buscar
        search_text = input('¿Qué palabras quieres buscar?\n')

        #recorrer los PDFS de la carpeta principal
        books_path = functions.get_PDFs(dir_path)

        for text_path in books_path:
            #path del libro actual  
            txt_name = str(int(t))+'_'
            #el path servirá para el archivo de texto
            txt_name += text_path.replace('./','').replace(' ','').replace('/','_').replace('.pdf','')+'.txt'
            scan_book(text_path,search_text,output_name=txt_name)        

        #recorrer todas las carpetas de un directorio
        sub_dir = functions.get_dirs(dir_path)
        for folder in sub_dir:

            folder_path = dir_path+folder
            #paths de los pdfs existentes
            books_path = functions.get_PDFs(folder_path)

            for text_path in books_path:
                #path del libro actual  
                #se agrega el tiempo para que sea único
                txt_name = str(int(t))+'_'
                #el path servirá para el archivo de texto
                txt_name += text_path.replace('./','').replace(' ','').replace('/','_').replace('.pdf','')+'.txt'
                scan_book(text_path,search_text,output_name=txt_name)

    else:
        print(main.__doc__)  

if __name__ == "__main__":
    import sys
    program_response = main(sys.argv[1:])
    if(program_response):
        print(program_response)
