from customtkinter import *
from tkinter import filedialog
from PIL import Image
import sys
import cv2

from Backend import Clip
from Backend import Grabar
from Entrenamiento_Ia import testeador

class Ventana():

    def __init__(self):

        self.app = CTk()
        self.Ancho = self.obtenerAnchoPantalla(self.app, 65)
        self.Largo = self.obtenerLargoPantalla(self.app, 65)

        self.app.geometry(f"{self.Ancho}x{self.Largo}")

        self.Reproducir = True # Varible empleada para detener el video si es deseado con un boton.
        self.Skip = None

        self.Grabacion = None

        #Paleta Colores

        self.colorFondo = '#373739'
        self.primerGris = "#19191a"
        self.segundoGris = "#19191a"
        self.textoGris = "#c6c6c6"

        self.colorRojo = "#ff0000"
        self.rojoOscuro = "#C20000"
        self.rojoHover = "#A50000"
        self.colorBlanco = "#FFFFFF"

        self.app.title("Fault Detector")
        self.app.after(201, lambda :self.app.iconbitmap('Frontend/Imagenes/Icono.ico'))

        self.pantallaCarga(self.app)
       
        self.app.mainloop()

    def obtenerAnchoPantalla(self, Elemento, Porcentaje, Ancho = None):

        if(Ancho == None):

            Ancho = Elemento.winfo_screenwidth()

        return Ancho * Porcentaje // 100

    def obtenerLargoPantalla(self, Elemento, Porcentaje, Largo = None):

        if(Largo == None):

            Largo = Elemento.winfo_screenheight()

        return Largo * Porcentaje // 100
    
    def obtenerAncho(self, Ancho, Porcentaje):

        return Ancho * Porcentaje // 100
    
    def obtenerLargo(self, Largo, Porcentaje):

        return Largo * Porcentaje // 100

    def pantallaCarga(self, Frame):

        Frame.rowconfigure(0, weight = 1)
        Frame.rowconfigure(1, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        anchoImagenFrame = self.obtenerAncho(self.Ancho, 100)
        largoImagenFrame = self.obtenerLargo(self.Largo, 80)

        Imagen = Image.open("Frontend/Imagenes/tarjetaRoja.png")

        Ancho, Largo = Imagen.size

        Ancho *= 0.5
        Largo *= 0.5

        imagenCTK = CTkImage(Imagen, size=(Ancho, Largo))

        Imagen = CTkImage(light_image = Image.open("Frontend/Imagenes/tarjetaRoja.png"), 
                          dark_image = Image.open("Frontend/Imagenes/tarjetaRoja.png"))
        
        contenedor = CTkLabel(master = Frame,
                              text = "",
                              image = imagenCTK)
        
        contenedor.grid(row = 0, column = 0)
        
        anchoCargarFrame = self.obtenerAncho(self.Ancho, 100)
        largoCargaFrame = self.obtenerLargo(self.Largo, 20)

        barraCarga = CTkProgressBar(master = Frame,
                                    width = self.obtenerAncho(self.Ancho, 20),
                                    height = self.obtenerLargo(self.Largo, 1.5),
                                    progress_color = self.rojoOscuro,
                                    mode = "determinate",
                                    determinate_speed = 0,
                                    orientation = "horizontal",
                                    )
        
        barraCarga.grid(row = 1, column = 0)

        barraCarga.set(0)
        
        def barraProgreso():

            valor = barraCarga.get()

            if(valor < 1):

                 valor += 0.012
                 barraCarga.set(valor)
                 Frame.after(6, barraProgreso)
            
            else:

                self.generarFrames(self.app)

        barraCarga.start()
        barraProgreso()        
        barraCarga.stop()            

    def generarFrames(self, Ventana):

        for widget in self.app.winfo_children():

            widget.destroy() 

        Ventana.rowconfigure(0, weight = 0)
        Ventana.rowconfigure(1, weight = 1)
        Ventana.rowconfigure(2, weight = 1)
        Ventana.columnconfigure(0, weight = 1)

        primerFrameAncho = self.obtenerAncho(self.Ancho, 100)
        primerFrameLargo = self.obtenerLargo(self.Largo, 5)

        self.segundoFrameAncho = self.obtenerAncho(self.Ancho, 100)
        self.segundoFrameLargo = self.obtenerLargo(self.Largo, 65)

        tercerFrameAncho = self.obtenerAncho(self.Ancho, 100)
        tercerFrameLargo = self.obtenerLargo(self.Largo, 30)

        primerFrame = CTkFrame(master = Ventana,
                               width = primerFrameAncho,
                               height = primerFrameLargo,
                               fg_color = self.primerGris)
        
        primerFrame.grid(row = 0, column = 0, sticky = "nsew")

        self.generarNavegacion(primerFrame, primerFrameAncho, primerFrameLargo)

        self.segundoFrame = CTkFrame (master = Ventana,
                            width = self.segundoFrameAncho,
                            height = self.segundoFrameLargo,
                            fg_color = self.colorFondo,
                            corner_radius = 0)

        self.segundoFrame.grid(row = 1, column = 0, sticky = "nsew")

        self.displayVideo(self.segundoFrame, self.segundoFrameAncho, self.segundoFrameLargo)

        tercerFrame = CTkFrame (master = Ventana,
                           width = tercerFrameAncho,
                           height = tercerFrameLargo,
                           fg_color = self.primerGris)
        
        tercerFrame.grid(row = 2, column = 0, sticky = "nsew")

        self.generarResultados(tercerFrame, tercerFrameAncho, tercerFrameLargo)

    def generarNavegacion(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 0)
        Frame.columnconfigure(0, weight = 0)

        Valores = ["Opciones", "Subir", "Generar Clip", "Detener", "Salir"]

        boton = CTkOptionMenu(master = Frame, 
                                values = Valores,
                                corner_radius = 0,
                                command = lambda selection : self.opcionesMenu(selection),
                                fg_color = self.colorRojo,
                                button_color = self.rojoOscuro,
                                button_hover_color = self.rojoHover
                                )   
                
        boton.grid(row = 0, column = 0)
        
    def opcionesMenu(self, Valor):

        if(Valor == "Subir"):

            self.obtenerVideo(self.segundoFrame, self.segundoFrameAncho, self.segundoFrameLargo)

        if(Valor == "Generar Clip"):

            Mensaje = CTkInputDialog(title = "Generar Clip",
                                     text = "Ingresa el link para generar clip: ",
                                     button_fg_color = self.colorRojo,
                                     button_hover_color = self.rojoHover
                                     )
            
            self.app.after(201, lambda: Mensaje.iconbitmap("Frontend/Imagenes/Icono.ico"))

            Direccion = str(Mensaje.get_input())
    
            if(len(Direccion) > 0):
                
                self.Grabacion = Clip.BrowserRecorder(Direccion)
                self.Grabacion.start_browser()
                
        elif(Valor == "Salir"):

            sys.exit()

    def detenerGrabacion(self):
        
        self.Grabacion.close_browser()

    def displayVideo(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 1)
        Frame.rowconfigure(1, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        primerFrameAncho = self.obtenerAncho(Ancho, 100)
        primerFrameLargo = self.obtenerLargo(Largo, 80)

        segundoFrameAncho = self.obtenerAncho(Ancho, 100)
        segundoFrameLargo = self.obtenerLargo(Largo, 20)
        
        primerFrame = CTkFrame(master = Frame,
                               width = primerFrameAncho,
                               height = primerFrameLargo,
                               corner_radius = 0)
        
        primerFrame.rowconfigure(0, weight = 1)
        primerFrame.columnconfigure(0, weight = 1)

        primerFrame.grid(row = 0, column = 0, sticky = "nsew")
        
        Imagen = Image.open("Frontend/Imagenes/Video.png")

        imagenAncho, imagenLargo = Imagen.size

        imagenAncho = self.obtenerAncho(imagenAncho, 30)
        imagenLargo = self.obtenerAncho(imagenLargo, 30)

        imagenCTK = CTkImage(Imagen, size=(imagenAncho, imagenLargo))

        contenedorImagen = CTkLabel(master = primerFrame,
                                    width = primerFrameAncho,
                                    height = primerFrameLargo,
                                    text = "",
                                    image = imagenCTK)
        
        contenedorImagen.grid(row = 0, column = 0, sticky = "nsew")

        segundoFrame = CTkFrame(master = Frame,
                                width = segundoFrameAncho,
                                height = segundoFrameLargo,
                                corner_radius = 0)
        
        segundoFrame.rowconfigure(0, weight = 1)
        segundoFrame.columnconfigure(0, weight = 1)
        
        segundoFrame.grid(row = 1, column =  0, sticky = "nsew")

        boton = CTkButton(master = segundoFrame,
                          width = self.obtenerAncho(segundoFrameAncho, 10),
                          height = self.obtenerLargo(segundoFrameLargo, 50),
                          fg_color = self.colorRojo,
                          hover_color =  self.rojoHover,
                          corner_radius = 0,
                          text = "Subir Clip",
                          font = ("Helvetica", 16),
                          command = lambda : self.obtenerVideo(Frame, Ancho, Largo))
        
        boton.grid(row = 0, column = 0)

    def obtenerVideo(self, Frame, Ancho, Largo):

        archivo = filedialog.askopenfilename(initialdir="/", 
                                             title="Seleccionar archivo", 
                                             filetypes=(("Archivos de video", ".mp4"), ("Archivos de video", ".avi")))
        print("Archivo seleccionado:", archivo)

        if(len(archivo) > 0):

            for widget in Frame.winfo_children():

                widget.destroy() 
            
            Resultados = testeador.predict_new_video_with_percentage(archivo)
            print(Resultados)

            captura = cv2.VideoCapture(archivo)   # Lectura del archivo de video.
            cantidadFotogramas = int(captura.get(cv2.CAP_PROP_FRAME_COUNT))
            tasaCambio = 1 / cantidadFotogramas
            
            #Reestructuracion del frame para crear un reproductor de video.

            Frame.rowconfigure(0, weight = 1)
            Frame.rowconfigure(1, weight = 1)
            Frame.columnconfigure(0, weight = 1)

            primerFrameAncho = self.obtenerAncho(Ancho, 100)
            primerFrameLargo = self.obtenerLargo(Largo, 90)

            segundoFrameAncho = self.obtenerAncho(Ancho, 100)
            segundoFrameLargo = self.obtenerLargo(Largo, 10)

            primerFrame = CTkFrame(master = Frame,
                                   width = primerFrameAncho,
                                   height = primerFrameLargo,
                                    )
            
            primerFrame.grid(row = 0, column = 0, sticky = "nsew")

            primerFrame.rowconfigure(0, weight = 1)
            primerFrame.columnconfigure(0, weight = 1)

            texto = CTkLabel(master = primerFrame,
                             text = "",
                             width = primerFrameAncho,
                             height = primerFrameLargo,
                             )
            
            texto.grid(row = 0, column = 0, sticky = "nsew")

            segundoFrame = CTkFrame(master = Frame,
                                    width = segundoFrameAncho,
                                    height = segundoFrameLargo,
                                    )
            segundoFrame.grid(row = 1, column = 0, sticky = "nsew")

            self.construirBotones(segundoFrame, segundoFrameAncho, segundoFrameLargo)

            self.visualizar(texto, captura, primerFrameAncho, primerFrameLargo, tasaCambio, 1)

    def construirBotones(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 0)
        Frame.rowconfigure(1, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        primerFrameAncho = self.obtenerAncho(Ancho, 100)
        primerFrameLargo = self.obtenerLargo(Largo, 20)

        segundoFrameAncho = self.obtenerAncho(Ancho, 100)
        segundoFrameLargo = self.obtenerLargo(Largo, 80)

        self.barraCarga = CTkProgressBar(master = Frame,
                                    width = primerFrameAncho,
                                    height = primerFrameLargo,
                                    progress_color = self.colorRojo,
                                    mode = "determinate",
                                    determinate_speed = 0,
                                    corner_radius = 0)
        
        self.barraCarga.grid(row = 0, column = 0, sticky = "nsew")

        segundoFrame = CTkFrame(master = Frame,
                                width = segundoFrameAncho,
                                height = segundoFrameLargo,
                                fg_color = self.colorFondo
                                )
        
        segundoFrame.grid(row = 1, column = 0, sticky = "nsew")

        #Creamos otro frame dentro de la barra de botones en caso de necesitar futuras integraciones de botones adicionales

        segundoFrame.rowconfigure(0, weight = 1)
        segundoFrame.columnconfigure(0, weight = 1)

        contenedorBotonesAncho =  self.obtenerAncho(segundoFrameAncho, 33.3)
        contenedorBotonesLargo = self.obtenerLargo(segundoFrameLargo, 100)

        botonesAncho =  self.obtenerAncho(contenedorBotonesAncho, 20)
        botonesLargo = self.obtenerLargo(contenedorBotonesLargo, 100)

        contenedorBotones = CTkFrame(master = segundoFrame,
                                     width = contenedorBotonesAncho,
                                     height = contenedorBotonesLargo)
        
        contenedorBotones.grid(row = 0, column = 0)

        contenedorBotones.rowconfigure(0, weight = 1)
        contenedorBotones.columnconfigure(0, weight = 1)
        contenedorBotones.columnconfigure(1, weight = 1)
        contenedorBotones.columnconfigure(2, weight = 1)

        atrasarIcono =  CTkImage(light_image = Image.open("Frontend/Imagenes/Atrasar.png"),
                        dark_image = Image.open("Frontend/Imagenes/Atrasar.png"),
                        size = (20, 20))
        
        regresarBoton = CTkButton(master = contenedorBotones,
                                  width = botonesAncho,
                                  height = botonesLargo,
                                  text = "",
                                  fg_color = self.primerGris,
                                  corner_radius = 0,
                                  image = atrasarIcono,
                                  command = lambda : self.saltar(False))
        
        inicioIcono = CTkImage(light_image = Image.open("Frontend/Imagenes/Inicio.png"), 
                                  dark_image = Image.open("Frontend/Imagenes/Inicio.png"),
                                  size = (20, 20))
        
        pausarBoton = CTkButton(master = contenedorBotones,
                                width = botonesAncho,
                                height = botonesLargo,
                                text = "",
                                fg_color = self.primerGris,
                                corner_radius = 0,
                                image = inicioIcono,
                                command = lambda : self.cambiarEstado(pausarBoton)
                                )
        
        adelantarIcono = CTkImage(light_image = Image.open("Frontend/Imagenes/Adelantar.png"), 
                                  dark_image = Image.open("Frontend/Imagenes/Adelantar.png"),
                                  size = (20, 20))        
        
        adelantarBoton = CTkButton(master = contenedorBotones,
                                   width = botonesAncho,
                                   height = botonesLargo,
                                   text = "",
                                   fg_color = self.primerGris,
                                   corner_radius = 0,
                                   image = adelantarIcono,
                                   command = lambda : self.saltar(True)
                                   )
        
        regresarBoton.grid(row = 0, column = 0)
        pausarBoton.grid(row = 0, column = 1, padx = 2)
        adelantarBoton.grid(row = 0, column = 2)

    def cambiarEstado(self, Widget):
       
        if(self.Reproducir == True):

            detenerIcono = CTkImage(light_image = Image.open("Frontend/Imagenes/Detener.png"), 
                                    dark_image = Image.open("Frontend/Imagenes/Detener.png"),
                                    size = (20, 20))

            Widget.configure(image = detenerIcono)

            self.Reproducir = False

        else:

            inicioIcono = CTkImage(light_image = Image.open("Frontend/Imagenes/Inicio.png"), 
                                    dark_image = Image.open("Frontend/Imagenes/Inicio.png"),
                                    size = (20, 20))

            Widget.configure(image = inicioIcono)

            self.Reproducir = True

    def saltar(self, Estado):
        
        if(Estado == False):
            
            self.Skip = False

        else:

            self.Skip = True           

    def visualizar(self, Widget, Video, Ancho, Largo, tasaCambio, primerIteracion):

        if (self.Reproducir == False): # Pausar video
             
            Widget.after(10, self.visualizar, Widget, Video, Ancho, Largo, tasaCambio, 0)
            return 
                     
        if(primerIteracion == 1): # Unicamente ocurre cuando el video se carga por primera vez.

            self.barraCarga.set(0)            
            self.barraCarga.start() # Volver a empezar mi barra de carga

        if(self.Skip == True):

            #Fotograma Actual

            fps = Video.get(cv2.CAP_PROP_FPS)
            adelantar = fps * 2 

            #Porcentaje Barra Actual

            valorPrevio = self.barraCarga.get()
            valorSiguiente = valorPrevio + (tasaCambio * (fps * 2))
            self.barraCarga.set(valorSiguiente)

            frameActual = Video.get(cv2.CAP_PROP_POS_FRAMES)
            Video.set(cv2.CAP_PROP_POS_FRAMES, frameActual + adelantar)

            self.Skip = None

        elif(self.Skip == False):

            #Fotograma Actual

            fps = Video.get(cv2.CAP_PROP_FPS)
            adelantar = fps * 2 

            #Porcentaje Barra Actual

            valorPrevio = self.barraCarga.get()
            valorSiguiente = valorPrevio - (tasaCambio * (fps * 2))
            self.barraCarga.set(valorSiguiente)

            frameActual = Video.get(cv2.CAP_PROP_POS_FRAMES)
            Video.set(cv2.CAP_PROP_POS_FRAMES, frameActual - adelantar)

            self.Skip = None

        ret, frame = Video.read()

        if not ret:

            Video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reinicia el video al principio
            ret, frame = Video.read()  # Lee el primer frame nuevamente
            self.barraCarga.set(0)

        if (ret == True):
            
            if (self.Reproducir == True):

                carga = self.barraCarga.get()
                valor = carga + tasaCambio
                self.barraCarga.set(valor)

                largoVideo, anchoVideo, _ = frame.shape

                #Calculo la proporcion del video en relacion al tamaño del label

                proporcionLargo = Largo / largoVideo
                proporcionAncho = Ancho / anchoVideo

                #Escojo el menor para mantener la relacion de aspecto, ya que de otra manera la imagen desborda el contenedor.

                escala = min(proporcionLargo, proporcionAncho)

                anchoNuevo = int(anchoVideo * escala)
                largoNuevo = int(largoVideo * escala)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                fotograma = Image.fromarray(frame)
                imagenCTk = CTkImage(light_image= fotograma, dark_image = fotograma, size = (anchoNuevo, largoNuevo))

                Widget.configure(image = imagenCTk)
                Widget.image = imagenCTk

                Widget.after(10, self.visualizar, Widget, Video, Ancho, Largo, tasaCambio, 0)   

    def generarResultados(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 1)
        Frame.columnconfigure(0, weight = 1)
        Frame.columnconfigure(1, weight = 1)

        frameAncho = self.obtenerAncho(Ancho, 50)
        frameLargo = self.obtenerLargo(Largo, 50)

        primerFrame = CTkFrame(master = Frame,
                               width = Ancho,
                               height = Largo, 
                               corner_radius = 0)
        
        primerFrame.grid(row = 0, column = 0, sticky = "nsew")

        primerFrame.rowconfigure(0, weight = 1)
        primerFrame.columnconfigure(0, weight = 1)

        texto = CTkTextbox(master = primerFrame,
                           width = frameAncho,
                           height = frameLargo,
                           font = ("Consolas", 16))
        
        texto.grid(row = 0, column  = 0, sticky = "nsew")

        texto.insert("0.0", "Fault Detector [Metrics]")
        
        segundoFrame = CTkFrame(master = Frame,
                                width = frameAncho,
                                height = frameLargo, 
                                fg_color = self.segundoGris,
                                corner_radius = 0)

        segundoFrame.grid(row = 0, column = 1, sticky = "nsew")
