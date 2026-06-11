#Aqui es donde corre todo el juego y se importan todas las funciones graficas y de logica, es el punto de entrada del juego

import pygame
pygame.init()
import clases
import constantes as ct
import mecanicas_menu   

pantalla = pygame.display.set_mode((ct.ANCHO, ct.ALTO), pygame.SCALED) #crea la ventana del juego con la resolución definida en constantes.py
pygame.display.set_caption("RUNMEAL")
reloj = pygame.time.Clock()
ejecutor = True


while ejecutor:
    #limpiar ventana primero
    pantalla.fill((0, 0, 0)) 
    
    #crear un evento vacío por defecto para evitar errores
    evento_actual = pygame.event.Event(pygame.USEREVENT) 
    
    #captura de eventos reales
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutor = False
        evento_actual = event #guardar el ultimo evento detectado
            
    #procesar el menu/juego con el evento seguro
    mecanicas_menu.menu(evento_actual, pantalla) 
    
    #actualizar la pantalla y mantener los FPS
    pygame.display.flip()  
    reloj.tick(ct.FPS) 

pygame.quit()