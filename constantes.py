import pygame
import sys
from clases import Boton, Slider, FondoAnimado
#SISTEMA ----------------------------------------------------------------------------------------------
#Resolucion
ANCHO = 1280
ALTO = 720
#FPS
FPS = 60
#Estados del juego
estado_juego = "menu"

#MENU ----------------------------------------------------------------------------------------------
#definicion de colores (Formato RGB)
COLOR_FONDO = (26, 26, 46)      #Azul muy oscuro
COLOR_BOTON = (15, 52, 96)      #Azul marino
COLOR_HOVER = (233, 69, 96)     #Rojo para cuando pasas el mouse
COLOR_TEXTO = (255, 255, 255)   #Blanco
COLOR_TITULO = (241, 196, 15)   #Dorado

#definicion de Fuentes (Tamaños)// PLACEHOLDERS por mientras
fuente_titulo = pygame.font.Font(None, 100)
fuente_subtitulo = pygame.font.Font(None, 60)
fuente_botones = pygame.font.Font(None, 40)
fuente_tabla = pygame.font.Font(None, 35)

#BOTONES PRINCIPALES
#Centramos los botones en X restando la mitad de su ancho (300/2 = 150)
centro_x = ANCHO // 2 - 150

btn_jugar = Boton(centro_x, 300, 300, 60, "JUGAR", fuente_botones, COLOR_BOTON, COLOR_HOVER)
btn_config = Boton(centro_x, 460, 300, 60, "CONFIGURACIÓN", fuente_botones, COLOR_BOTON, COLOR_HOVER)
btn_salir = Boton(centro_x, 540, 300, 60, "SALIR", fuente_botones, COLOR_BOTON, COLOR_HOVER)
btn_reiniciar = Boton(centro_x, 350, 300, 60, "REINICIAR", fuente_botones, COLOR_BOTON, COLOR_HOVER)
btn_menu = Boton(centro_x, 430, 300, 60, "MENÚ PRINCIPAL", fuente_botones, COLOR_BOTON, COLOR_HOVER)

#BOTON PARA VOLVER ATRAS
btn_volver = Boton(30, ALTO - 90, 200, 50, "Volver Atrás", fuente_botones, (127, 140, 141), (149, 165, 166))

#CONTROLES DE CONFIGURACION 
slider_musica = Slider(400, 300, 300, 20, 0.5) #50% por default
slider_sonido = Slider(400, 400, 300, 20, 0.75) #75% por default
btn_pantalla = Boton(centro_x, 540, 300, 60, "Pantalla Completa", fuente_botones, COLOR_BOTON, COLOR_HOVER)

#BOTON DE SALIDA
btn_si = Boton(ANCHO//2 - 160, 600, 140, 60, "SÍ", fuente_botones, (39, 174, 96), (46, 204, 113))
btn_no = Boton(ANCHO//2 + 20, 600, 140, 60, "NO", fuente_botones, (192, 57, 43), (231, 76, 60))

#JUGADOR ----------------------------------------------------------------------------------------------
jugador_pos = [ANCHO//2, ALTO//2]
jugador_velocidad = 5

#AUDIO ----------------------------------------------------------------------------------------------
pygame.mixer.init() 

try:
    #cargar el ambiente del menú al iniciar el juego
    pygame.mixer.music.load("audio/AmbienteMenu.mp3")
    pygame.mixer.music.play(-1) # -1 es para bucle infinito
    pygame.mixer.music.set_volume(slider_musica.valor) 
    
    #cargar los efectos de sonido
    sonido_disparo = pygame.mixer.Sound("audio/disparo.mp3")
    sonido_explosion = pygame.mixer.Sound("audio/enemigoDerrotado.mp3")
    sonido_gameover = pygame.mixer.Sound("audio/gameover.mp3")
    sonido_hit_jugador = pygame.mixer.Sound("audio/golpeaJugador.mp3")
except FileNotFoundError:
    print("Advertencia: No se encontraron los archivos de audio en la carpeta 'audio'.")
    sonido_disparo = sonido_explosion = sonido_gameover = None

#FONDOS -------------------------------------------------------------------------------------------
#menu: imagen estática escalada a la pantalla
try:
    fondo_menu = pygame.image.load("graficos/menufondo.png")
    fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO, ALTO))
except FileNotFoundError:
    fondo_menu = None #por si ocurre un error de ruta

#gameplay: animación (carpeta, milisegundos por frame, ancho, alto)
fondo_gameplay = FondoAnimado("graficos/gameplay", 80, ANCHO, ALTO)