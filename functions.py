from shutil import Error
import pdf2image 
import os
import glob
import PyPDF2
import sys
import pytesseract
import cv2

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

def get_book_name(book_path:str) -> str:
    """Recibe el path de un libro y retorna su nombre
    sin la terminación .pdf"""
    #tomo sólo el nombre del libro
    if(('/' in book_path) or ('\\' in book_path)):
        book_name = book_path.split('/')[-1]
        book_name = book_name.split('\\')[-1]
    else:
        book_name = book_path

    #le quito el tipo de dato
    book_name = book_name.replace('.pdf','')
    return book_name

#################
# OCR: Voy a hacer que esta función aplique
# un OCR sobre el contenido de la página enviada 
###############

#necesito saber si las fotos ya existen
#se asume que si la primera foto existe, entonces
# el libro ya fue escaneado
def there_are_imgs(book_path:str) -> bool:
    """Recibe el path de un libro y verifica
    si ya se han generado sus imágenes para no volver
    a hacerlo"""
    #consigo el inicio para el nombre de la imagen
    book_img_name = get_book_name(book_path)
    #agrego la terminación de la primera página
    book_img_name += '_page_1.jpg'
    #verifico si esa imagen existe en la carpeta de imágenes
    imgs_folder = 'book_imgs/'
    return os.path.isfile(imgs_folder+book_img_name)

#necesito generar las fotos del libro
def create_book_images(book_path:str) -> bool:
    """Genera las imágenes de un libro dado.
    Retorna verdadero si todas las imágenes se pudieron
    crear satisfactoriamente"""
    try:
        #consigo las páginas del libro
        pages = pdf2image.convert_from_path(pdf_path=book_path, dpi=350)
        #consigo el nombre del libro para
        #los nombres de las imgs
        book_img_name = get_book_name(book_path)
        #declaro la carpeta de las imágenes
        imgs_folder = 'book_imgs/'
        #creo un for para recorrer cada imagen
        num_pages = get_PDF_numPages(book_path)
        for i,page in enumerate(pages):
            current_page = i+1
            drawProgressBar(percent=current_page/num_pages)
            book_img_path = imgs_folder+book_img_name+'_page_'+str(i+1)+ ".jpg"  
            page.save(book_img_path, "JPEG")
        return True
    except Error:
        print(Error)
        return False

#separa la página en párrafos
def mark_region(image_path:str):
    """Encuentra las regiones donde se encuentra
    el texto para que el ocr se enfoque sólo en esas
    zonas"""
    #abre la imagen
    im = cv2.imread(image_path)
    #lo convierte a gris
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    #vuelve la imagen borrosa
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    #binarización
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)

    # dilata para unir zonas cercanas
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # encuentra los contornos de las manchas
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    #para las páginas en blanco
    if(len(cnts)<1):
        return []
    #esta lista almacenará los rectángulos que
    #envuelven las zonas con texto
    line_items_coordinates = []
    last_y = cv2.boundingRect(cnts[0])[1]
    for i,c in enumerate(cnts):
        x,y,w,h = cv2.boundingRect(c)
        #si dos rectángulos están en la misma y
        #deben estar en la misma línea

        if((y-last_y)**2<25 and i>0):
            last_c = line_items_coordinates[-1]
            lx = last_c[0][0]
            line_items_coordinates[-1] = [(lx,y), (x+w, y+h)]            
        else:
            # almacenan las coordenadas de la esquina 
            # superior izquierda y la inferior derecha
            line_items_coordinates.append([(x,y), (x+w, y+h)])
        last_y=y
    return line_items_coordinates

#tengo que recorrer todas las fotos de un mismo libro
#para retornar el texto mediante el OCR
def ocr_img(img_path:str) ->str:
    """Recibe el path de una imagen y realiza un
    escaneo OCR para retornar el texto"""
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # load the original image
    paragraphs = mark_region(img_path)
    image = cv2.imread(img_path)
    text = ''
    for pi in paragraphs:
        upleft_corner = pi[0]
        downright_corner = pi[1]
        #tomo sólo la sección del párrafo
        img = image[upleft_corner[1]:downright_corner[1],
                upleft_corner[0]:downright_corner[0]]    
        #evito espacios en blanco
        if(0 not in img.shape):
            #se convierte a blanco y negro
            ret,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY)
            text += str(pytesseract.image_to_string(thresh1, config='--psm 6'))
    return text
    

#leer el contenido de un archivo PDF
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
    """Retorna el párrafo donde se encontró la frase
    buscada."""
    paragraph = ''
    phrase = str(phrase).lower()
    text = str(text).lower()

    #split por palabra buscada
    resultados = text.split(phrase)
    num_resultados = len(resultados)
    if(num_resultados>1):
        for i in range(num_resultados):
            add_char = 100
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

#escanea el libro completo con OCR
def scan_book_with_OCR(path:str,phrase:str):
    #conseguir el número de páginas
    num_pages = get_PDF_numPages(path)
    #verifico si las imágenes del libro existen
    if(not there_are_imgs(path)):
        print('Se crearán imágenes del libro...')
        #si no hay imágenes, hay que crearlas
        if(create_book_images(path)):
            print('El libro se escaneó por primera vez y se generó una imagen de cada página')
        else:
            return 'El buscador inteligente tuvo problemas con este libro'

    #esta variable tendrá el texto de cada página
    book_content = ''
    #esta variable tendrá los resultados encontrados
    info =''
    for page in range(num_pages):
        #los índices de páginas empiezan en 1
        current_page = page+1
        #dibujo una barra de progreso por si acaso
        drawProgressBar(percent=current_page/num_pages)
        #declaro la carpeta de las imágenes
        imgs_folder = 'book_imgs/'
        #consigo el nombre del libro
        nombre = get_book_name(path)
        #texto de página para el nombre de la imagen
        pagina = '_page_'
        #escaneo la imagen del libro
        book_content = ocr_img(imgs_folder+nombre+pagina+str(current_page)+'.jpg')
        #obtengo el texto que estoy buscando
        match = get_paragraph(phrase,text=book_content)
        if(match):
            info += 'Página '+str(current_page)+'\n'
            info += '...'+match+'...\n\n'
    return info


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
    

