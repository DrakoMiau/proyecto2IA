import pyglet
from pyglet.gl import Config
import math


#LOS ALAMOS 6X6
DIM = 6
CELL = 120
WIDTH = DIM * CELL 
HEIGHT = DIM * CELL

#Colores RGBA
LIGHT_COLOR = (238, 238, 210, 255)
DARK_COLOR = (118, 150, 86, 255)

IMAGES = {}

def cargar_imagenes():
    global IMAGES
    piezas = ['Pb', 'Cb', 'Tb', 'Rb', 'Kb', 'Pn', 'Cn', 'Tn', 'Rn', 'Kn']
    for p in piezas:
        try:
            img_abstract = pyglet.image.load(f'assets/{p}.png')
            img_data = img_abstract.get_image_data()
            
            pitch = img_data.width * 4 
            
            data = img_data.get_data('BGRA', pitch) 

            img = pyglet.image.ImageData(
                img_data.width, 
                img_data.height, 
                'BGRA', 
                data 
            )
            
            texture = img.get_texture()
            texture.width = CELL
            texture.height = CELL
        
            IMAGES[p] = texture
        except FileNotFoundError:
            print(f"ERROR: No se encontró la imagen para la pieza {p}.")
            pass 
    return IMAGES

cargar_imagenes()

class GUI(pyglet.window.Window):
    
    
    def __init__(self, juego):
        super().__init__(width = WIDTH, 
                         height = HEIGHT, 
                         caption = "Los Alamos Chess",
                         config = Config(alpha_size=8, depth_size=24, double_buffer=True))
        
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        self.juego = juego
        self.batch = pyglet.graphics.Batch()

        #Animación
        self.pieza_animando = None
        self.origen_logico = None
        self.destino_logico = None
        self.pos_destino_px = None
        self.distancia_total_px = 0.0
        self.tiempo_transcurrido = 0.0
        
        self.velocidad_animacion_px_s = 800.0 # Velocidad en píxeles/segundo
        self.altura_max_elevacion = CELL * 0.4 # Altura máxima de elevación

        #Intervalo
        pyglet.clock.schedule_interval(self._logica_turno_ia, 0.5)

    def _posicion_logica_a_pixeles(self, r, c):
        x = c * CELL
        y = (DIM - 1 - r) * CELL

        return (x, y)
    
    def on_draw(self):
        self.clear()
        
        for r in range(DIM):
            for c in range(DIM):
                color = LIGHT_COLOR if (r + c) % 2 == 0 else DARK_COLOR
                pyglet.shapes.Rectangle(c * CELL, (DIM - 1 - r) * CELL, 
                                        CELL, CELL, color=color[:3]).draw() #No Alpha
        
        #Piezas estáticas
        for r in range(DIM):
            for c in range(DIM):
                pieza = self.juego.tablero.casillas[r][c]
                # No dibujar la pieza en la casilla de origen si está en animación
                if pieza and not (self.pieza_animando and (r, c) == self.origen_logico):
                    simbolo = pieza.simbolo
                    if simbolo in IMAGES:
                        x, y = self._posicion_logica_a_pixeles(r, c)
                        #IMAGES[simbolo].blit(x, y)
                        sprite = pyglet.sprite.Sprite(IMAGES[simbolo], x, y)
                        sprite.opacity = 255
                        sprite.draw()
                        
        #Dibujar el sprite de animación
        if self.pieza_animando:
            self.pieza_animando.draw()
        
        # Muestra el estado actual del juego si ha terminado
        if not self.juego.en_juego:
            label = pyglet.text.Label(f"FIN: {self.juego.tablero.estado_del_juego().upper()}",
                                      font_size = 32, x = WIDTH // 2, y = HEIGHT // 2, 
                                      anchor_x = 'center', anchor_y = 'center', color = (255, 0, 0, 255))
            label.draw()


    
    def _logica_turno_ia(self, dt):
        
        # El juego ya terminó, solo dibujar
        if not self.juego.en_juego or self.pieza_animando:
            return

        jugador_actual = self.juego.IA_Blanca if self.juego.tablero.turno_actual == "blanco" else self.juego.IA_Negra

        # Asumo que Jugador.obtener_mejor_movimiento devuelve (evaluacion, mejor_mov)
        mejor_mov = jugador_actual.obtener_mejor_movimiento(self.juego.tablero)

        

        if mejor_mov is None:
            self.juego.verificar_estado()
            pyglet.clock.unschedule(self._logica_turno_ia)
            return

        self._iniciar_animacion(mejor_mov)

    
    def _iniciar_animacion(self, mejor_mov):
        
        self.origen_logico, self.destino_logico = mejor_mov
        r_origen, c_origen = self.origen_logico
        r_destino, c_destino = self.destino_logico
        
        pieza_actual = self.juego.tablero.casillas[r_origen][c_origen]
        simbolo = pieza_actual.simbolo
        
        imagen_pieza = IMAGES[simbolo]
        self.pieza_animando = pyglet.sprite.Sprite(imagen_pieza) 
        
        x_inicio, y_inicio = self._posicion_logica_a_pixeles(r_origen, c_origen)
        self.pieza_animando.x = x_inicio
        self.pieza_animando.y = y_inicio
        
        self.pos_destino_px = self._posicion_logica_a_pixeles(r_destino, c_destino)
        
        dx_total = self.pos_destino_px[0] - x_inicio
        dy_total = self.pos_destino_px[1] - y_inicio
        self.distancia_total_px = math.sqrt(dx_total**2 + dy_total**2)
        self.tiempo_transcurrido = 0.0

        pyglet.clock.schedule_interval(self._mover_sprite, 1 / 120.0) # Usar alta frecuencia para fluidez (120 FPS)
    

    def _mover_sprite(self, dt):
        
        if not self.pieza_animando or self.origen_logico is None:
            pyglet.clock.unschedule(self._mover_sprite)
            return

        x_inicio, y_inicio = self._posicion_logica_a_pixeles(*self.origen_logico)
        x_destino, y_destino = self.pos_destino_px
        
        tiempo_total_movimiento = self.distancia_total_px / self.velocidad_animacion_px_s
        self.tiempo_transcurrido += dt
        
        progreso = self.tiempo_transcurrido / tiempo_total_movimiento
        
        if progreso >= 1.0:
            self._finalizar_animacion(x_destino, y_destino)
            return

        base_x = x_inicio + (x_destino - x_inicio) * progreso
        base_y = y_inicio + (y_destino - y_inicio) * progreso
        
        # Elevación Parabólica (Efecto de "levantar la pieza")
        # Función: y = 4 * h_max * (p - p^2)
        p = progreso
        elevacion = 4 * self.altura_max_elevacion * (p - p**2)
        
        self.pieza_animando.x = base_x
        self.pieza_animando.y = base_y + elevacion
        #self.pieza_animando.draw()

    def _finalizar_animacion(self, x_final, y_final):
        
        pyglet.clock.unschedule(self._mover_sprite)
        self.pieza_animando.delete()
        self.pieza_animando = None
        
        self.juego.tablero.mover_pieza(self.origen_logico, self.destino_logico) 
        
        self.juego.tablero.cambiar_turno()
        
        self.origen_logico = None
        self.destino_logico = None
