import pygame
import constantes as ct
from clases import Boton, Slider
import mecanicas_game as game 
def dibujar_texto(texto, fuente, color, superficie, x, y, centrado = False):
        img_texto = fuente.render(texto, True, color)
        rect_texto = img_texto.get_rect()
        if centrado:
            rect_texto.center = (x, y)
        else:
            rect_texto.topleft = (x, y)
        superficie.blit(img_texto, rect_texto)

def menu(event, pantalla):
#ELECTOR DE ESTADOS DEL JUEGO     
    if ct.estado_juego == "menu":
        if ct.btn_jugar.manejar_evento(event):
            game.reiniciar_stats()
            pygame.mixer.music.load("audio/MusicaGameplay.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(ct.slider_musica.valor) 
            ct.estado_juego = "gameplay"    
        if ct.btn_config.manejar_evento(event):
            ct.estado_juego = "MENU_CONFIGURACION"
        if ct.btn_salir.manejar_evento(event):
            ct.estado_juego = "MODAL_SALIR"
    #MENU CONFIGURACION
    elif ct.estado_juego == "MENU_CONFIGURACION":
        ct.slider_musica.manejar_evento(event)
        ct.slider_sonido.manejar_evento(event)
        
        #actualizar volumen de la música en tiempo real
        pygame.mixer.music.set_volume(ct.slider_musica.valor)

        #pantalla completa
        if ct.btn_pantalla.manejar_evento(event):
            pygame.display.toggle_fullscreen()
            
    if ct.btn_volver.manejar_evento(event):
        ct.estado_juego = "menu"

    #MODAL SALIR
    elif ct.estado_juego == "MODAL_SALIR":
        if ct.btn_si.manejar_evento(event):
            event.type = pygame.QUIT #crea un evento de salida para cerrar el juego
        if ct.btn_no.manejar_evento(event):
            ct.estado_juego = "menu" #regresa al menu
       
    elif ct.estado_juego == "game_over":
        if ct.btn_reiniciar.manejar_evento(event):
            game.reiniciar_stats()
            ct.estado_juego = "gameplay"
        if ct.btn_menu.manejar_evento(event):
            game.reiniciar_stats()
            ct.estado_juego = "menu"

    #LOGICA-GAME OVER 
    elif ct.estado_juego == "game_over":
        if ct.btn_reiniciar.manejar_evento(event):
            game.reiniciar_stats()
            pygame.mixer.music.load("audio/MusicaGameplay.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(ct.slider_musica.valor) 
            ct.estado_juego = "gameplay"
            
        if ct.btn_menu.manejar_evento(event):
            game.reiniciar_stats()
            pygame.mixer.music.load("audio/AmbienteMenu.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(ct.slider_musica.valor)
            ct.estado_juego = "menu"

    #PARTE VISUAL DEL MENU ----------------------------------------------------------------------------------------------------------------------------
        
    if ct.estado_juego == "menu":
        if ct.fondo_menu: pantalla.blit(ct.fondo_menu, (0, 0))
    #titulo centrado
        dibujar_texto("RUNMEAL", ct.fuente_titulo, ct.COLOR_TITULO, pantalla, ct.ANCHO//2, 150, centrado = True)
    #dibujar botones
        ct.btn_jugar.dibujar(pantalla)
        ct.btn_config.dibujar(pantalla)
        ct.btn_salir.dibujar(pantalla)

    elif ct.estado_juego == "gameplay":
        game.gameplay(pantalla, event)


    elif ct.estado_juego == "MENU_CONFIGURACION":
        if ct.fondo_menu: pantalla.blit(ct.fondo_menu, (0, 0))
        dibujar_texto("CONFIGURACIÓN", ct.fuente_subtitulo, ct.COLOR_TITULO, pantalla, ct.ANCHO//2, 150, centrado = True)
        
        dibujar_texto("Música:", ct.fuente_botones, ct.COLOR_TEXTO, pantalla, 250, 300)
        ct.slider_musica.dibujar(pantalla)
            
        dibujar_texto("Sonidos:", ct.fuente_botones, ct.COLOR_TEXTO, pantalla, 250, 400)
        ct.slider_sonido.dibujar(pantalla)

        ct.btn_pantalla.dibujar(pantalla)
        ct.btn_volver.dibujar(pantalla)

    elif ct.estado_juego == "MODAL_SALIR":
        if ct.fondo_menu: pantalla.blit(ct.fondo_menu, (0, 0))
    #para hacer el "pop-up" primero dibujar el menu principal de fondo
        dibujar_texto("RUN-MEAL", ct.fuente_titulo, ct.COLOR_TITULO, pantalla, ct.ANCHO//2, 150, centrado = True)
        ct.btn_jugar.dibujar(pantalla)
        ct.btn_config.dibujar(pantalla)
        ct.btn_salir.dibujar(pantalla)

    #crear una capa oscura semi-transparente
        capa_oscura = pygame.Surface((ct.ANCHO, ct.ALTO))
        capa_oscura.set_alpha(200) #nivel de transparencia (0-255)
        capa_oscura.fill((0, 0, 0))
        pantalla.blit(capa_oscura, (0,0))
            
    #dibujamos el cuadro de la pregunta
        rect_modal = pygame.Rect(ct.ANCHO//2 - 250, 500, 500, 250)
        pygame.draw.rect(pantalla, ct.COLOR_BOTON, rect_modal, border_radius = 15)
        pygame.draw.rect(pantalla, ct.COLOR_HOVER, rect_modal, 4, border_radius = 15)
        
        dibujar_texto("¿Deseas salir del juego?", ct.fuente_subtitulo, ct.COLOR_TEXTO, pantalla, ct.ANCHO//2, 400, centrado = True)
            
        ct.btn_si.dibujar(pantalla)
        ct.btn_no.dibujar(pantalla)

    #game over
    elif ct.estado_juego == "game_over":
        
        pantalla.fill((20, 5, 5)) #Fondo rojo muy oscuro
        
        dibujar_texto("GAME OVER", ct.fuente_titulo, (233, 69, 96), pantalla, ct.ANCHO//2, 150, centrado = True)
        
        #mostrar la puntuación
        dibujar_texto(f"Puntuación Final: {game.puntuacion}", ct.fuente_subtitulo, ct.COLOR_TEXTO, pantalla, ct.ANCHO//2, 250, centrado = True)
        
        ct.btn_reiniciar.dibujar(pantalla)
        ct.btn_menu.dibujar(pantalla)