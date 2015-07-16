# -*- coding: utf-8 -*-

import pygame

from sys import exit
from os import environ, listdir
from Tkinter import Tk, Label
from ttk import Combobox, Button
from tkMessageBox import showwarning

from src import *

pygame.init()

pygame.mixer.init(channels=8)

class Menu(object):
    KONAMI_CODE = [273, 273, 274, 274, 276, 275, 276, 275, 98, 97, 13]
    ATTEMPTS = []
    
    def __init__(self):
        # Create the window
        environ['SDL_VIDEO_WINDOW_POS'] = 'center'
        self.clock = pygame.time.Clock()
        
        logo = pygame.image.load("res/logo/logo.png")
        
        self.screen = pygame.display.set_mode((800, 576))
        pygame.display.set_caption('BattleTank')
        pygame.display.set_icon(logo)
        
        # Background image
        self.background = pygame.image.load("res/backgrounds/background.png").convert()
        self.background = pygame.transform.scale(self.background, (800, 576))
        
        title_font = pygame.font.Font("res/fonts/Joystix.ttf", 60)
        
        self.builder = LevelBuilder(self)
        self.game_window = GameWindow(self)
                
        self.secret_music = pygame.mixer.Sound("res/sounds/congratulations.wav")
        self.cheats_on = False
        
        # Change to True if you want the intro animation
        self.first_time = False
        
        # Begin the main loop
        while True:
            
            # If it's the first time, we run the intro animation
            if self.first_time:
                
                pygame.event.set_allowed(pygame.QUIT)
                
                for i in range(255):
                    for event in pygame.event.get():
                
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit(0)
                    
                    self.screen.fill((0,0,0))
                    
                    self.background.set_alpha(i)
                    self.screen.blit(self.background, (0,0))
                    
                    pygame.display.update()
                    
                    # At 17 FPS, it takes 14 seconds to finish
                    self.clock.tick(17)
                    
                self.first_time = False
            
            # Begin the normal flow
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                
                # Ignore this
                if event.type == pygame.KEYDOWN:
                    self.ATTEMPTS.append(event.key)
                    for attempt, correct in zip(self.ATTEMPTS, self.KONAMI_CODE):
                        if attempt != correct:
                            self.ATTEMPTS = []
                            break
                    else:
                        if self.ATTEMPTS == self.KONAMI_CODE:
                            # You cheater
                            self.secret_music.play(0)
                            self.cheats_on = True
                            
                            
            self.screen.blit(self.background, (0, 0))
            
            self.screen.blit(title_font.render("Battle", 1, (0,47,0)), (250, 100))
            self.screen.blit(title_font.render("Tank", 1, (0,47,0)), (300, 160))
            
            self.make_button("Begin Game", 
                            (250, 300, 300, 50),
                            ((206, 174, 125), (142, 125, 72)),
                            funcion=lambda: LevelsWindow(self))
            
            self.make_button(u"Design Level", 
                            (250, 360, 300, 50), 
                            ((206, 174, 125), (142, 125, 72)),
                            funcion=lambda: self.call_to("LevelBuilder"))
            
            self.make_button(u"Informacion", 
                            (250, 420, 300, 50), 
                            ((206, 174, 125), (142, 125, 72)),
                            funcion=self.mostrarInfo)
            
            pygame.display.update()
            self.clock.tick(60)

    def call_to(self, function, params=None):        
        self.ATTEMPTS = []
        
        if function == "LevelBuilder":
            self.builder.create_level()
        else:
            self.game_window.begin_game(params, self.cheats_on)
        
        # Turn off the mixer, as there could be some sounds still playing
        pygame.mixer.stop()
        

    def make_button(self, texto, rect, colores, funcion=None):
        # TODO: Translate this function
                
        mouse = pygame.mouse.get_pos()      # Posicion del mouse
        click = pygame.mouse.get_pressed()  # Cual boton del mouse esta apretado
        
        # Por default, el boton esta en estado no presionado
        boton = pygame.draw.rect(self.screen, colores[0], rect)
        
        if boton.collidepoint(mouse):  # El mouse esta dentro del boton
            # Cambiamos la imagen
            boton = pygame.draw.rect(self.screen, colores[1], rect)
            
            # Si el boton esta siendo presionado, ejecutamos la funcion asociada
            if click[0]:
                if funcion is not None:
                    funcion()
            
            
        # Dibujamos un rectangulo alrededor del boton
        pygame.draw.rect(self.screen, (0, 0 ,0), (rect[0] - 1, rect[1] - 1, rect[2] + 2, rect[3] + 2), 2)
        

        # Dibujamos el texto en el boton
        # Times New Roman, tamaño 20
        tipoLetra = pygame.font.SysFont("timesnewroman", 20)
        superTexto = tipoLetra.render(texto, 1, (0, 0, 0))

        # Sacamos el rectangulo alrededor del texto y modificamos sus coordenadas
        textoRect = superTexto.get_rect()
        textoRect.center = ( (rect[0] + (rect[2] / 2), rect[1] + (rect[3] / 2)) )

        self.screen.blit(superTexto, textoRect)  # "Mete" el texto dentro del boton

    
    def mostrarInfo(self):
        window = Tk()
        window.title("General Info")
        
        icon = PhotoImage(file=os.getcwd() + '/res/logo/logo.gif')
        window.tk.call("wm", "iconphoto", window._w, icon)
        
        # TODO: Translate this
        texto = """
        En el antiguo planeta Irata, la guerra se ha desatado una vez más.
        Los silurios han vuelto a atacar al pueblo Iratense con sus poderosos tanques,  con el fin de destruir el Corazon de Mee-Ul.
        Tu mision, proteger el Corazon y destruir a todos los enemigos que encuentres!

        POR LA GLORIA DE IRATA!

        Controles del juego:
        * Teclas direccionales: Mueves el tanque.
        * Barra espaciadora: Disparas una vez.
        * Tu tanque se mejora cada 5 muertes.
        * Tu corazon puede recibir 4 disparos antes de destruirse

        Uso del constructor de niveles:
        * Haz click en la imagen del bloque que desees poner.
        * Mueve el bloque dentro del area de mapa (sector gris).
        * Si la imagen del bloque se encuentra en verde, significa que puedes poner el bloque en esa posicion.
        * Para posicionar el bloque, vuelve a hacer click.
        * Para eliminar tu mapa actual, presiona el boton "Limpiar Mapa".
        * Para guardar tu mapa actual, presiona el boton "Guardar Mapa".

        Restricciones con respecto al guardado de nivel:
        * El nivel debe contener, como minimo, el Corazon, el Jugador y un agujero de enemigos.
        * El nombre del mapa debe ser de menos de 15 caracteres.
        * Cada mapa debe tener por lo menos un enemigo.
        """
        
        title = Label(window, text=texto, justify=LEFT)
        title.grid(row=0, column=0)
        
        button = Button(window, text="OK", command=window.destroy)
        button.grid(row=1, column=0)
        window.mainloop()
        
        


class LevelsWindow(Tk):
    def __init__(self, menu):
        Tk.__init__(self)
        
        self.title("Pick a level")
        
        icon = PhotoImage(file=os.getcwd() + '/res/logo/logo.gif')
        self.tk.call("wm", "iconphoto", self._w, icon)
        
        self.eval('tk::PlaceWindow %s center' % self.winfo_pathname(self.winfo_id()))
        
        self.levels = [file[:-4] for file in listdir("res/levels")]
        self.protocol("WM_DELETE_WINDOW", self.shutdownTTK)
        
        if not self.levels:  # No levels
            self.withdraw()
            tkMessageBox.showwarning("Error", 'There doesn\'t seem to be any levels saved. Create one pressing the "Design Level" button!')
            self.shutdownTTK()
            
        else:
            self.menu = menu
            
            self.value = StringVar()
            self.levels_list = Combobox(self, textvariable=self.value, state='readonly')
            
            self.levels_list['values'] = self.levels
            self.levels_list.current(0)
            self.levels_list.grid(column=0, row=0)
            
            self.button = Button(self, text="Begin Level", command=self.begin_level)
            self.button.grid(column=0, row=1)
            self.mainloop()
    
            
            
    def begin_level(self):
        level = self.levels_list.get()
        self.shutdownTTK()
        self.menu.call_to("GameWindow", level)
    
    
    def shutdownTTK(self):
        # For some unholy reason, TTK won't shut down when we destroy the window
        # so we have to explicitly kill it.
        self.eval('::ttk::CancelRepeat')
        self.destroy()
        
if __name__ == "__main__":
    Menu()
