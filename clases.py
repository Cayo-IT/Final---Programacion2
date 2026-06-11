import pygame
import random
import os
# Clases para el MENU y CONFIGURACION
class Boton:
    """Clase para crear botones interactivos en pantalla."""
    def __init__(self, x, y, ancho, alto, texto, fuente, color_normal, color_hover):
        #guardar las dimensiones y posición del botón
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.fuente = fuente
        self.color_normal = color_normal  #color cuando no se toca
        self.color_hover = color_hover    #color cuando el mouse pasa por encima
        self.color_actual = self.color_normal
        self.texto_color = (255, 255, 255) #blanco

    def dibujar(self, pantalla):
        #dibujar el rectangulo del boton en la pantalla
        pygame.draw.rect(pantalla, self.color_actual, self.rect, border_radius=8)
        #dibujamr un borde para que se vea mejor
        pygame.draw.rect(pantalla, (233, 69, 96), self.rect, 2, border_radius=8)
        
        #Renderizar el texto (crear la imagen del texto)
        texto_superficie = self.fuente.render(self.texto, True, self.texto_color)
        #Centrar el texto dentro del boton
        texto_rect = texto_superficie.get_rect(center=self.rect.center)
        pantalla.blit(texto_superficie, texto_rect)

    def manejar_evento(self, evento):
        """Verifica si el botón fue presionado o si el mouse está encima."""
        pos_mouse = pygame.mouse.get_pos()
        
        #cambiar el color si el mouse está sobre el botón (Efecto Hover)
        if self.rect.collidepoint(pos_mouse):
            self.color_actual = self.color_hover
            #si el evento es un clic izquierdo (botón 1) del mouse
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                return True #el botón fue presionado
        else:
            self.color_actual = self.color_normal
           
        return False #no fue presionado
class Slider:
    """Clase para crear barras ajustables (como las de volumen)."""
    def __init__(self, x, y, ancho, alto, valor_inicial):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.valor = valor_inicial #Valor entre 0.0 y 1.0 (0% a 100%)
        self.arrastrando = False

    def dibujar(self, pantalla):
        #dibujar el fondo del slider (gris oscuro)
        pygame.draw.rect(pantalla, (50, 50, 50), self.rect, border_radius=5)
        
        #dibujamos la parte "llena" del slider (color rojo/rosa)
        ancho_lleno = int(self.rect.width * self.valor)
        rect_lleno = pygame.Rect(self.rect.x, self.rect.y, ancho_lleno, self.rect.height)
        pygame.draw.rect(pantalla, (233, 69, 96), rect_lleno, border_radius=5)
        
        #dibujar el "boton" indicador del slider
        pygame.draw.circle(pantalla, (255, 255, 255), (self.rect.x + ancho_lleno, self.rect.y + self.rect.height // 2), self.rect.height)

    def manejar_evento(self, evento):
        """Permite arrastrar el slider para cambiar su valor."""
        pos_mouse = pygame.mouse.get_pos()
        
        #si hace clic dentro del área del slider
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(pos_mouse):
                self.arrastrando = True
                
        #si soltamos el clic
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            self.arrastrando = False
            
        #si estamos moviendo el mouse mientras arrastramos
        if self.arrastrando:
            #calcular el nuevo valor basado en la posición X del mouse
            nuevo_x = max(self.rect.x, min(pos_mouse[0], self.rect.x + self.rect.width))
            self.valor = (nuevo_x - self.rect.x) / self.rect.width
class Bala:
    def __init__(self, x, y, direccion):
        self.pos = [x, y]  #posición actual de la bala 
        self.direccion = direccion  #dirección de movimiento 
        self.velocidad = 10  #velocidad de la bala
        self.radio = 5  #tamaño de la bala 
        
    def mover(self):
        #Actualiza la posición según dirección y velocidad
        self.pos[0] += self.direccion[0] * self.velocidad
        self.pos[1] += self.direccion[1] * self.velocidad

    def dibujar(self, superficie):
        #COLOR: Amarillo 
        pygame.draw.circle(
            superficie, 
            (255, 255, 0), 
            (int(self.pos[0]), int(self.pos[1])), 
            self.radio
        )

class BalaEnemiga:
    def __init__(self, x, y, direccion):
        self.pos = [x, y]
        self.direccion = direccion
        self.velocidad = 7 
        self.radio = 5
        self.color = (255, 140, 0) #color naranja para distinguirlas

    def mover(self):
        self.pos[0] += self.direccion[0] * self.velocidad
        self.pos[1] += self.direccion[1] * self.velocidad

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, (int(self.pos[0]), int(self.pos[1])), self.radio)

class Enemigo:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.velocidad = random.randint(2, 5) #velocidad de caída
        #velocidad lateral aleatoria al nacer (diagonal)
        self.vel_x = random.choice([-3, -2, 2, 3]) 
        self.radio = 15
        self.color = (50, 200, 50)
        
        #sistema de disparo independiente
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()
        self.cooldown_disparo = random.randint(500, 1000) 

    def mover(self):
        #movimiento hacia abajo
        self.pos[1] += self.velocidad
        #movimiento lateral
        self.pos[0] += self.vel_x
        
        #rebotar en los bordes laterales de la pantalla (1280 es el ancho)
        if self.pos[0] <= self.radio or self.pos[0] >= 1280 - self.radio:
            self.vel_x *= -1 #invierte la dirección

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, (int(self.pos[0]), int(self.pos[1])), self.radio)
    
class FondoAnimado:
    """Carga una carpeta de imágenes y las anima en bucle."""
    def __init__(self, carpeta, velocidad_animacion, ancho, alto):
        self.frames = []
        try:
            if os.path.exists(carpeta):
                archivos = sorted(os.listdir(carpeta))
                for archivo in archivos:
                    if archivo.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                        ruta = os.path.join(carpeta, archivo)
                        img = pygame.image.load(ruta) 
                        img = pygame.transform.scale(img, (ancho, alto))
                        self.frames.append(img)
                print(f"EXITO: Se cargaron {len(self.frames)} fotogramas de la carpeta {carpeta}")
            else:
                print(f"ERROR: No se encontró la carpeta '{carpeta}'.")
        except Exception as e:
            print(f"Error cargando animación: {e}")

        self.frame_actual = 0
        self.velocidad_animacion = velocidad_animacion
        self.tiempo_ultimo_frame = pygame.time.get_ticks()

    def dibujar(self, pantalla):
        if not self.frames: 
            return 
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_ultimo_frame > self.velocidad_animacion:
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.tiempo_ultimo_frame = tiempo_actual
        pantalla.blit(self.frames[self.frame_actual], (0, 0))