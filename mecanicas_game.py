import pygame
import random
import constantes as ct
from clases import Bala, Enemigo, BalaEnemiga 

balas = [] 
balas_enemigas = []
enemigos = []
puntuacion = 0
vidas = 3
tiempo_ultimo_disparo = 0
tiempo_ultimo_enemigo = 0

def reiniciar_stats():
    """Limpia las listas y reinicia los valores para una nueva partida."""
    global balas, balas_enemigas, enemigos, puntuacion, vidas #modifica las variables
    balas.clear()
    balas_enemigas.clear() #limpiamos la pantalla de balas enemigas
    enemigos.clear()
    puntuacion = 0
    vidas = 3
    ct.jugador_pos = [ct.ANCHO//2, ct.ALTO//2]

def gameplay(pantalla, event):
    global balas, balas_enemigas, enemigos, puntuacion, vidas, tiempo_ultimo_disparo, tiempo_ultimo_enemigo 
    
    tiempo_actual = pygame.time.get_ticks()

    #movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and ct.jugador_pos[1] > 20: ct.jugador_pos[1] -= ct.jugador_velocidad
    if keys[pygame.K_s] and ct.jugador_pos[1] < ct.ALTO - 20: ct.jugador_pos[1] += ct.jugador_velocidad
    if keys[pygame.K_a] and ct.jugador_pos[0] > 20: ct.jugador_pos[0] -= ct.jugador_velocidad
    if keys[pygame.K_d] and ct.jugador_pos[0] < ct.ANCHO - 20: ct.jugador_pos[0] += ct.jugador_velocidad

    #mecánica de disparo del jugador
    if keys[pygame.K_SPACE]:
        if tiempo_actual - tiempo_ultimo_disparo > 200: 
            nueva_bala = Bala(ct.jugador_pos[0], ct.jugador_pos[1], (0, -1))
            balas.append(nueva_bala)
            #sonido de disparo modificable con el slider
            if ct.sonido_disparo:
                ct.sonido_disparo.set_volume(ct.slider_sonido.valor)
                ct.sonido_disparo.play()
            tiempo_ultimo_disparo = tiempo_actual

    #generar enemigos 
    if tiempo_actual - tiempo_ultimo_enemigo > 1000: 
        nuevo_enemigo = Enemigo(random.randint(20, ct.ANCHO - 20), -20)
        nuevo_enemigo.velocidad += (puntuacion // 100) 
        enemigos.append(nuevo_enemigo)
        tiempo_ultimo_enemigo = tiempo_actual

    #actualizar posiciones y disparos enemigos
    for bala in balas[:]:
        bala.mover()
        if bala.pos[1] < 0: balas.remove(bala)

    for bala_e in balas_enemigas[:]:
        bala_e.mover()
        if bala_e.pos[1] > ct.ALTO: balas_enemigas.remove(bala_e)

    for enemigo in enemigos[:]:
        enemigo.mover()
        
        #logica para que el enemigo dispare
        if tiempo_actual - enemigo.tiempo_ultimo_disparo > enemigo.cooldown_disparo:
            #Disparan hacia abajo 
            nueva_bala_e = BalaEnemiga(enemigo.pos[0], enemigo.pos[1], (0, 1))
            balas_enemigas.append(nueva_bala_e)
            enemigo.tiempo_ultimo_disparo = tiempo_actual #reinicia su temporizador
            
        if enemigo.pos[1] > ct.ALTO: enemigos.remove(enemigo)

    #colisiones 
    for enemigo in enemigos[:]:
        #colisión enemigo vs balas jugador
        for bala in balas[:]:
            distancia_bala = ((bala.pos[0] - enemigo.pos[0])**2 + (bala.pos[1] - enemigo.pos[1])**2)**0.5
            if distancia_bala < (bala.radio + enemigo.radio):
                if bala in balas: balas.remove(bala)
                if enemigo in enemigos: enemigos.remove(enemigo)
                puntuacion += 10 
                #sonido de choque de balas modificable con el slider
                if ct.sonido_explosion:
                    ct.sonido_explosion.set_volume(ct.slider_sonido.valor)
                    ct.sonido_explosion.play()
                break 

        #colision enemigo vs jugador
        distancia_jugador = ((ct.jugador_pos[0] - enemigo.pos[0])**2 + (ct.jugador_pos[1] - enemigo.pos[1])**2)**0.5
        if distancia_jugador < (20 + enemigo.radio): 
            if enemigo in enemigos: enemigos.remove(enemigo)
            vidas -= 1
            if vidas > 0:
                #si sobrevive al golpe, suena el hit
                if ct.sonido_hit_jugador:
                    ct.sonido_hit_jugador.set_volume(ct.slider_sonido.valor)
                    ct.sonido_hit_jugador.play()
            elif ct.estado_juego == "gameplay": 
                ct.estado_juego = "game_over"
                pygame.mixer.music.stop() 
                if ct.sonido_gameover:
                    ct.sonido_gameover.set_volume(ct.slider_sonido.valor)
                    ct.sonido_gameover.play()

    #colision balas enemigas vs jugador
    for bala_e in balas_enemigas[:]:
        distancia_bala_jugador = ((ct.jugador_pos[0] - bala_e.pos[0])**2 + (ct.jugador_pos[1] - bala_e.pos[1])**2)**0.5
        if distancia_bala_jugador < (20 + bala_e.radio):
            if bala_e in balas_enemigas: balas_enemigas.remove(bala_e)
            vidas -= 1
            if vidas > 0:
                #si sobrevive al balazo, suena el hit
                if ct.sonido_hit_jugador:
                    ct.sonido_hit_jugador.set_volume(ct.slider_sonido.valor)
                    ct.sonido_hit_jugador.play()
            elif ct.estado_juego == "gameplay":
                ct.estado_juego = "game_over"
                pygame.mixer.music.stop() 
                if ct.sonido_gameover:
                    ct.sonido_gameover.set_volume(ct.slider_sonido.valor)
                    ct.sonido_gameover.play()

    #dibujar en pantalla
    ct.fondo_gameplay.dibujar(pantalla)
    
    pygame.draw.circle(pantalla, (255, 0, 0), (int(ct.jugador_pos[0]), int(ct.jugador_pos[1])), 20)
    for bala in balas: bala.dibujar(pantalla)
    for bala_e in balas_enemigas: bala_e.dibujar(pantalla)
    for enemigo in enemigos: enemigo.dibujar(pantalla)

    #interfaz: vidas y puntuacion
    texto_vidas = ct.fuente_botones.render(f"Vidas: {vidas}", True, (233, 69, 96)) 
    pantalla.blit(texto_vidas, (20, 30)) 
    
    texto_puntos = ct.fuente_botones.render(f"Puntos: {puntuacion}", True, ct.COLOR_TEXTO)
    pantalla.blit(texto_puntos, (ct.ANCHO - 200, 30))