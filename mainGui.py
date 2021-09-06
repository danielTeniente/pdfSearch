import tkinter.constants 
import functions
import tkinter
import tkinter.font

# 
# DANIEL DIAZ
# Función principal para la interfaz gráfica
# El programa debe contener un cuadro de texto
# para introducir el término de búsqueda.
# El botón empezará el proceso de escanera            
# los archivos PDF y los resultados se 
# desplegarán sobre un label. #

raiz = tkinter.Tk()
raiz.title('Buscador de referencias')
raiz.iconbitmap("favicon.ico")


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

##############################
# FRAME PRINCIPAL #
##############################

#label de título para los resultados
lbResultTitle = tkinter.Label(frmMain,
    text='Resultados:',font=fontContent)
lbResultTitle.grid(row=3,column=0,pady=20)

#frame para los resultados
frmResults = tkinter.Frame(frmMain)
frmResults.grid(row=4,column=0,pady=25,padx=15)
#frmResults.config(background='white')


##############################
# FRAME RESULTADOS  #
##############################

#label para mostrar los resultados
txtResults = tkinter.Text(frmResults,
    font=fontContent,width=50,height=5)
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
    new_text = txtSearch.get()
    txtResults.delete(1.0,tkinter.constants.END)
    txtResults.insert(tkinter.constants.END,chars=new_text)

#botón de búsqueda
btnSearch = tkinter.Button(frmMain,
    text='Buscar',font=fontContent,
    command=press_search_btn)
btnSearch.grid(row=2,column=0,pady=10)


raiz.mainloop()

