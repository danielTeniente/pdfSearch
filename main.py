# imprimir el texto de un libro como AI
import functions

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
                path='.',name=output_name)):
                print('Grave Error al extraer información')
    print()
    if(got_txt):
        print('Resultados encontrados y almacenados en:',output_name)

    

#path de la carpeta que será analizada
dir_path ='./Referencias/cripto/'
#paths de los pdfs existentes
books_path = functions.get_PDFs(dir_path)
#lo que se va a buscar
search_text = 'bitcoin'

for text_path in books_path:
    #path del libro actual  
    #el path servirá para el archivo de texto
    txt_name = text_path.replace('./','').replace('/','_').replace('.pdf','')+'.txt'
    scan_book(text_path,search_text,output_name=txt_name)