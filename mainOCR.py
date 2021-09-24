import functions

#recibo el path de un libro, creo las imágenes y 
#escaneo con el OCR para guardar el resultado en
#un archivo de texto

def scan_book(path,phrase,output_name='text.txt'):
    #conseguir el número de páginas
    num_pages = functions.get_PDF_numPages(path)
    #info para el usuario
    print('Libro:',path)
    print('Extrayendo texto...')
    #esta variable tendrá el texto de cada página
    book_content = ''
    #verifico si las imágenes del libro existen
    if(not functions.there_are_imgs(path)):
        print('Se crearán imágenes del libro...')
        if(functions.create_book_images(path)):
            print('El libro se escaneó por primera vez y se generó una imagen de cada página')
        else:
            return False
    
    #verifica si se generó un txt
    got_txt = False
    #escaneo el libro página por página
    for page in range(num_pages):
        current_page = page+1
        functions.drawProgressBar(percent=current_page/num_pages)
        #declaro la carpeta de las imágenes
        imgs_folder = 'book_imgs/'
        nombre = functions.get_book_name(path)
        pagina = '_page_'
        #escaneo la imagen del libro
        book_content = functions.ocr_img(imgs_folder+nombre+pagina+str(current_page)+'.jpg')
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
    return True

def main(args):
    """
    [ES]
    Uso:
    python main.py 'libro' 
    Parámetros:
    libro: dirección o nombre de la carperta
        donde se almacenan los PDFs. Si el nombre de la carpeta
        tiene espacios, debes usar '' para engolbarlo.
    Ejemplos:
    python main.py Referencias
    python main.py software.pdf
    """
    if(len(args)==1):
        pdf_path =str(args[0])
        phrase = input('Qué quieres buscar \n')
        scan_book(pdf_path,phrase)

    else:
        print(main.__doc__) 

if __name__ == "__main__":
    import sys
    program_response = main(sys.argv[1:])
    if(program_response):
        print(program_response)        