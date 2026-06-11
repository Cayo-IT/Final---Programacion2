# Final---Programacion2
Este es el proyecto final del curso de Programacion 2 

-----------------------------
Bienvenido! 
El contenido de este repositorio es sobre un juego creado para proyecto final de la clase de programacion 2.
Este juego fue desarrollado por 3 colaboradores los cuales fueron:
- Cesar Osvaldo Diaz Martinez
- Julio Cesar Salazar Montijo
- Carlos Omar Sanchez Torrescano
  
-----------------------------
RunMeal es el nombre de nuestro juego el cual esta inspirado por el genero del tipo bullet-hell 
en el cual su jugabilidad se trata que apareces en el medio y tienes que eliminar enemigos, la meta es
intentar eliminar a la maxima cantidad de enemigos y obtener una puntuacion alta.

## Caracteristicas
El juego cuenta con un menú principal interactivo y diversas mecánicas desarrolladas desde cero usando Pygame:
* *Escalado de Dificultad Dinámico:* Por cada 100 puntos obtenidos, la velocidad de los enemigos aumenta, exigiendo mejores reflejos del jugador.
* *Sistema de Entidades Autónomas:* Los enemigos cuentan con movimiento lateral aleatorio y su propio sistema de recarga para disparar proyectiles de manera independiente.
* *Sistema de Audio:* Música de ambiente y acción que cambia según el estado del juego, junto con efectos de sonido (SFX) para disparos, daño y explosiones.
* *Configuración:* Interfaz con sliders interactivos para ajustar el volumen de la música y los efectos, además de soporte para modo de Pantalla Completa.

## Controles 
- Arriba: `W`
- Izquierda: `A`
- Abajo: `S`
- Derecha: `D`
- Disparar: `Barra espaciadora`
- Interactuar con el menu: `Click izquierdo del Mouse`

## Estructura y Arquitectura del Código
El proyecto fue diseñado aplicando principios de Programación Orientada a Objetos (POO) y una arquitectura modular para separar la lógica, la interfaz y las entidades:

* `main.py` / `Nucleo_principal.py`: Punto de entrada del programa y bucle principal seguro de captura de eventos.
* `mecanicas_game.py`: Motor lógico del gameplay. Maneja físicas, sistema de vidas, puntajes y la detección matemática de colisiones circulares.
* `mecanicas_menu.py`: Enrutador de la máquina de estados. Controla el renderizado de la UI (Menú, Configuración, Game Over y Modal de Salida) y las transiciones musicales.
* `clases.py`: Definición de las clases principales.
* `constantes.py`: Archivo de configuración global que almacena paletas de colores, fuentes, instanciación de recursos multimedia y variables compartidas.

## Requisitos y Dependencias
Para poder ejecutar este proyecto en tu máquina local, necesitas tener instalado lo siguiente:
* Python 3.0 (o la mas reciente) 
* Librería Pygame (`pip install pygame`)

## Cómo ejecutar el juego
1. Clona este repositorio en tu computadora.
2. Asegúrate de que las carpetas de recursos (`/audio` y `/graficos`) estén en el mismo directorio que los scripts.
3. Abre una terminal en la ruta del proyecto.
4. Ejecuta el archivo principal: `main.py`.
