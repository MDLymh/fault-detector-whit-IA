from customtkinter import *
from tkinter import filedialog
from PIL import Image
import sys
import cv2

class Ventana():

    def __init__(self):

        self.app = CTk()
        self.Ancho = self.obtenerAnchoPantalla(self.app, 65)
        self.Largo = self.obtenerLargoPantalla(self.app, 65)

        self.app.geometry(f"{self.Ancho}x{self.Largo}")

        #Paleta Colores

        self.colorFondo = '#373739'
        self.primerGris = "#19191a"
        self.segundoGris = "#19191a"
        self.textoGris = "#c6c6c6"

        self.colorRojo = "#ff0000"
        self.rojoOscuro = "#C20000"
        self.colorBlanco = "#FFFFFF"

        self.app.title("Fault Detector")
        self.app.after(201, lambda :self.app.iconbitmap('Imagenes/Icono.ico'))

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

        Imagen = Image.open("Imagenes/tarjetaRoja.png")

        Ancho, Largo = Imagen.size

        Ancho *= 0.5
        Largo *= 0.5

        imagenCTK = CTkImage(Imagen, size=(Ancho, Largo))

        Imagen = CTkImage(light_image = Image.open("Imagenes/tarjetaRoja.png"), 
                          dark_image = Image.open("Imagenes/tarjetaRoja.png"))
        
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
                                    orientation = "horizontal",
                                    )
        
        barraCarga.grid(row = 1, column = 0)

        barraCarga.set(0)
        
        def barraProgreso():

            valor = barraCarga.get()

            if(valor < 1):

                 valor += 0.006
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

        segundoFrameAncho = self.obtenerAncho(self.Ancho, 100)
        segundoFrameLargo = self.obtenerLargo(self.Largo, 65)

        tercerFrameAncho = self.obtenerAncho(self.Ancho, 100)
        tercerFrameLargo = self.obtenerLargo(self.Largo, 30)

        primerFrame = CTkFrame(master = Ventana,
                               width = primerFrameAncho,
                               height = primerFrameLargo,
                               fg_color = self.primerGris)
        
        primerFrame.grid(row = 0, column = 0, sticky = "nsew")

        self.generarNavegacion(primerFrame, primerFrameAncho, primerFrameLargo)

        segundoFrame = CTkFrame (master = Ventana,
                            width = segundoFrameAncho,
                            height = segundoFrameLargo,
                            fg_color = self.colorFondo,
                            corner_radius = 0)

        segundoFrame.grid(row = 1, column = 0, sticky = "nsew")

        self.displayVideo(segundoFrame, segundoFrameAncho, segundoFrameLargo)

        tercerFrame = CTkFrame (master = Ventana,
                           width = tercerFrameAncho,
                           height = tercerFrameLargo,
                           fg_color = self.primerGris)
        
        tercerFrame.grid(row = 2, column = 0, sticky = "nsew")

        self.generarResultados(tercerFrame, tercerFrameAncho, tercerFrameLargo)

    def generarNavegacion(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 0)
        Frame.columnconfigure(0, weight = 0)

        Valores = ["Opciones", "Subir", "Salir"]

        boton = CTkOptionMenu(master = Frame, 
                                values = Valores,
                                corner_radius = 0,
                                command = lambda selection : self.opcionesMenu(selection),
                                fg_color = self.colorRojo,
                                button_color = self.rojoOscuro
                                )   
                
        boton.grid(row = 0, column = 0)
        
    def opcionesMenu(self, Valor):

        if(Valor == "Opciones"):

            self.obtenerVideo()

        elif(Valor == "Salir"):

            sys.exit()

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
        
        Imagen = Image.open("Imagenes/Video.png")

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

            captura = cv2.VideoCapture(archivo)   # Lectura del archivo de video.

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
            
            self.visualizar(texto, captura, primerFrameAncho, primerFrameLargo)

    def construirBotones(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 0)
        Frame.rowconfigure(1, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        primerFrameAncho = self.obtenerAncho(Ancho, 100)
        primerFrameLargo = self.obtenerLargo(Largo, 30)

        segundoFrameAncho = self.obtenerAncho(Ancho, 100)
        segundoFrameLargo = self.obtenerLargo(Largo, 70)

        primerFrame = CTkFrame(master = Frame,
                               width = primerFrameAncho,
                               height = primerFrameLargo,
                               fg_color = "red")
        
        primerFrame.grid(row = 0, column = 0, sticky = "nsew")

        segundoFrame = CTkFrame(master = Frame,
                                width = segundoFrameAncho,
                                height = segundoFrameLargo,
                                )
        
        segundoFrame.grid(row = 1, column = 0, sticky = "nsew")

        segundoFrame.rowconfigure(0, weight = 1)
        segundoFrame.columnconfigure(0, weight = 1)
        segundoFrame.columnconfigure(1, weight = 1)
        segundoFrame.columnconfigure(2, weight = 2)

        anchoContenedores =  self.obtenerAncho(segundoFrameAncho, 33.3)
        largoContenedores = self.obtenerLargo(segundoFrameLargo, 100)

        anchoBotones =  self.obtenerAncho(anchoContenedores, 20)
        largoBotones = self.obtenerLargo(largoContenedores, 100)


        cotenedoresBotones = []

        for i in range(3):

            Contenedor = CTkFrame(master = segundoFrame,
                                             height = anchoContenedores,
                                             width = largoContenedores)
            
            #if((i + 1) % 2 == 0):

            #Es requerido alinear los dos botones aldeaños al central para evitar tener los botones tan dispersos
    
            Contenedor.grid(row = 0, column = i, sticky = "nsew")

            cotenedoresBotones.append(Contenedor)
       
        regresarBoton = CTkButton(master = cotenedoresBotones[0], 
                                  width = anchoBotones,
                                  height = largoBotones,
                                  text = "",
                                  fg_color = self.primerGris,
                                  corner_radius = 0)
        
        reanudarBoton = CTkImage(light_image = Image.open("Imagenes/Inicio.png"), 
                                  dark_image = Image.open("Imagenes/Inicio.png"),
                                  size = (20, 20))
        
        pausarBoton = CTkButton(master = cotenedoresBotones[1],
                                width = anchoBotones,
                                height = largoBotones,
                                text = "",
                                fg_color = self.primerGris,
                                corner_radius = 0,
                                image = reanudarBoton,
                                command = lambda : self.cambiarEstado(Frame)
                                )
        
        adelantarBoton = CTkButton(master = cotenedoresBotones[2],
                                   width = anchoBotones,
                                   height = largoBotones,
                                   text = "",
                                   fg_color = self.primerGris,
                                   corner_radius = 0)
        
        regresarBoton.grid(row = 0, column = 0)
        pausarBoton.grid(row = 0, column = 1)
        adelantarBoton.grid(row = 0, column = 2)

    def cambiarEstado(self, Frame):

        pass

    def visualizar(self, Widget, Video, Ancho, Largo):

        ret, frame = Video.read()

        if not ret:

            Video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reinicia el video al principio
            ret, frame = Video.read()  # Lee el primer frame nuevamente

        if (ret == True):

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
            Widget.after(10, self.visualizar, Widget, Video, Ancho, Largo)         

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

if __name__ == "__main__":

    Ventana()
