import tkinter.constants 
import functions
import tkinter
import tkinter.font
import tkinter.ttk
import tkinter.messagebox 

# 
# DANIEL DIAZ
# Función principal para la interfaz gráfica
# El programa debe contener un cuadro de texto
# para introducir el término de búsqueda.
# El botón empezará el proceso de escanera            
# los archivos PDF y los resultados se 
# desplegarán sobre un label. #

###AVISO PARA EL USUARIO
print('####################')
print('PANEL DE PROGRESO')
print('####################')

####################
# VARIABLES Y CONSTANTES    
###################

#directorio donde se guardarán los libros
DIR_PATH = 'Referencias'


raiz = tkinter.Tk()
raiz.title('Buscador de referencias')
raiz.iconbitmap("./imgs/favicon.ico")


#creación del frame_principal
frmMain = tkinter.Frame(raiz)
#el frame_principal se expande con la ventana
frmMain.pack(fill='both',expand=True)

##############################
# FRAME PRINCIPAL #
##############################
#fuente para el título principal
fontMain = tkinter.font.Font(size=25, weight=tkinter.font.BOLD)

#Título del programa
lbTitulo = tkinter.Label(frmMain,text='Buscador de referencias',font=fontMain)
lbTitulo.grid(row=0,column=0)

#frame para el formulario de búsqueda
frmForm = tkinter.Frame(frmMain)
frmForm.grid(row=1,column=0)

##############################
# FRAME FORMULARIO #
##############################

#font para el texto del contenido
fontContent = tkinter.font.Font(size=15)

#label para preguntar palabras
lbAsk = tkinter.Label(frmForm,
    text='¿Qué palabras quieres buscar?',
    font=fontContent)
lbAsk.grid(row=0,column=0)

#entrada para las palabras clave
txtSearch = tkinter.Entry(frmForm,
    font=fontContent)
txtSearch.grid(row=0,column=1,padx=10,pady=10)

#etiqueta para pedir seleccionar un libro
lbAsk = tkinter.Label(frmForm,
    text='Selecciona un libro',
    font=fontContent)
lbAsk.grid(row=1,column=0)

#lista desplegable de los libros disponibles
#libros en la carpeta principal
books_path = functions.get_PDFs(DIR_PATH)
#libros de las carpetas hijas
sub_dir = functions.get_dirs(DIR_PATH)
for folder in sub_dir:
    #se agrega el símbolo para indicar directorio
    folder_path = DIR_PATH+'/'+folder
    #paths de los pdfs existentes
    books_path += functions.get_PDFs(folder_path)
fontList = tkinter.font.Font(size=12)
cmbBookList = tkinter.ttk.Combobox(frmForm,
    values=books_path,
    width=40,font=fontList,
    state='readonly')
cmbBookList.grid(row=1,column=1)

##############################
# FRAME PRINCIPAL #
##############################

#label de título para los resultados
lbResultTitle = tkinter.Label(frmMain,
    text='Resultados:',font=fontContent)
lbResultTitle.grid(row=3,column=0,pady=20)

#frame para los resultados
frmResults = tkinter.Frame(frmMain)
frmResults.grid(row=5,column=0,pady=25,padx=15)
#frmResults.config(background='white')

##############################
# FRAME RESULTADOS  #
##############################

#label para mostrar los resultados
txtResults = tkinter.Text(frmResults,
    font=fontContent,width=75,height=15)
txtResults.grid(row=1,column=0)
#scrollbar para los resultados
scrollResult = tkinter.Scrollbar(frmResults,
    command=txtResults.yview)
scrollResult.grid(row=1,column=1,sticky="nsew")
txtResults.config(yscrollcommand=scrollResult.set)

##############################
# FRAME PRINCIPAL #
##############################
#función que ejecutará el botón
def press_search_btn():
    #elimina el contenido del cuadro de texto
    txtResults.delete(1.0,tkinter.constants.END)
    #toma el contenido de combobox
    selected_book = cmbBookList.get()
    #toma las palabras a buscar
    search_text = txtSearch.get()
    #realiza la búsqueda sólo si se ha seleccionado
    #un libro y se ha escrito palabra clave
    if(len(search_text)>0 and selected_book!=''):
        #escribe el nombre del libro en el cuadro de texto
        txtResults.insert(tkinter.constants.END,
                        chars=selected_book+'\n')
        #nombre del archivo de texto donde se guardará la búsqueda
        #save results optional
        #txt_name = selected_book.replace('./','').replace(' ','').replace('/','_').replace('.pdf','.txt')
        print(selected_book)
        #resultado de la búsqueda
        resultados = functions.scan_book(selected_book,search_text)
        #sólo si hay coincidencia se agrega contenido
        if(len(resultados)>0):
            #save results optional
            #content = txt_name+'\n'
            content = resultados
        else:
            content = 'No se ha encontrado información.'
        #imprime los resultados en pantalla
        txtResults.insert(tkinter.constants.END,
            chars=content)
        #save results optional
        #if(functions.write_text(content,'./searching',txt_name)):
            #print('\nGuardado archivo de texto:',txt_name)
        print()
            
        #desbloquea el botón para otra búsqueda
        #btnSearch['state'] = 'normal'

def press_OCR_btn():
    #elimina el contenido del cuadro de texto
    txtResults.delete(1.0,tkinter.constants.END)
    #toma el contenido de combobox
    selected_book = cmbBookList.get()
    #toma las palabras a buscar
    search_text = txtSearch.get()
    #realiza la búsqueda sólo si se ha seleccionado
    #un libro y se ha escrito palabra clave
    if(len(search_text)>0 and selected_book!=''):
        result=tkinter.messagebox.askquestion('Búsqueda inteligente',
            'La búsqueda inteligente tarda más tiempo\n'+
            'para poder leer mejor el contenido.\n'+
            '¿Quiere continuar?')
        if(result=='yes'):
            #escribe el nombre del libro en el cuadro de texto
            txtResults.insert(tkinter.constants.END,
                            chars=selected_book+'\n')
            #se imprime el path del libro en consola
            print(selected_book)
            #resultado de la búsqueda
            resultados = functions.scan_book_with_OCR(selected_book,search_text)
            #sólo si hay coincidencia se agrega contenido
            if(len(resultados)>0):
                #save results optional
                #content = txt_name+'\n'
                content = resultados
            else:
                content = 'No se ha encontrado información.'
            #imprime los resultados en pantalla
            txtResults.insert(tkinter.constants.END,
                chars=content)
            #save results optional
            #if(functions.write_text(content,'./searching',txt_name)):
                #print('\nGuardado archivo de texto:',txt_name)
            print()

#botón de búsqueda
btnSearch = tkinter.Button(frmMain,
    text='Buscar',font=fontContent,
    command=press_search_btn)
btnSearch.grid(row=2,column=0,pady=10)

#botón de búsqueda con OCR
btnOCR = tkinter.Button(frmMain,
    text='Búsqueda inteligente',font=fontContent,
    command=press_OCR_btn)
btnOCR.grid(row=6,column=0,pady=10)

raiz.mainloop()

