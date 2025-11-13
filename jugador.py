#aqui hay que poner todos los agentes de IA
from tablero import Tablero, Rey
from utils import Utils

class Jugador:
    
    def __init__(self, color, profundidad = 5, func_eval = "material"):

        self.color = color
        self.profundidad = profundidad

        self.VALOR_MATE = 1e6
        
        #Funciones de Evaluación. Por defecto, ventaja de material.
        '''
            material: Ventaja de Material
            centro: Control del centro del tablero (4x4)

        '''
        self.fncs_eval = {
            "material" : self.func_material_eval,
            "centro" : self.func_centro_eval,
            "rey" : self.func_rey_eval
        }

        #Función de Evaluación elegida.
        self.evaluar_estado = self.fncs_eval[func_eval]

    def obtener_mejor_movimiento(self, tablero):
        
        '''
            EntryPoint
            - Estado (Tablero) actual
            - Profundidad
            - Alpha
            - Beta
            - Maximiza
        '''
        final_eval, mejor_mov = self.minimax_ab(tablero, self.profundidad, float("-inf"), float("inf"), True)

        print(F"(DEBUG) Evaluación Final: {final_eval}")
        return mejor_mov
    
    def estado_terminal(self, tablero):

        '''
            Turno Actual = Color jugador Actual y estado de Jaque Mate -> Turno anterior era rival. Ganó rival.
            Estado "tablas" (Empate): Nada.
            Caso contrario, No es estado terminal
        '''
        estado_actual = tablero.estado_del_juego()
        if estado_actual == "jaque_mate":
            if tablero.turno_actual == self.color:
                #Perdió, manco.
                return -self.VALOR_MATE
            else:
                #Ganó. Ya era hora.
                return self.VALOR_MATE
        elif estado_actual == "tablas":
            return 0.0
        
        return None


    def minimax_ab(self, tablero, profundidad, alpha, beta, turno_max):

        #Return: (Mejor_evaluación, Mejor_Movimiento).
        if profundidad == 0 or tablero.estado_del_juego() != "en_juego":
            return (self.evaluar_estado(tablero), None)
        
        mejor_mov = None
        color_actual = tablero.turno_actual

        movimientos = Utils.obtener_todos_movimientos(tablero, color_actual)

        if not movimientos:
            return (self.evaluar_estado(tablero), None)
        
        #MINIMAX ALPHA BETA PRUNNING.
        #No hay necesidad de implementar maximize y minimize de manera separada. EZ.

        #Maximiza.
        if turno_max:
            max_eval = float("-inf")

            for mov in movimientos:
                nuevo_tablero = tablero.copiar_tablero()
                
                nuevo_tablero.mover_pieza(mov[0], mov[1])
                nuevo_tablero.cambiar_turno()

                eval, _ = self.minimax_ab(nuevo_tablero, profundidad - 1, alpha, beta, False)

                if eval > max_eval:
                    max_eval, mejor_mov = eval, mov

                alpha = max(alpha, eval)
                if beta < alpha:
                    return (max_eval, mejor_mov)
            
            return (max_eval, mejor_mov)
        
        #Minimiza.
        else:
            min_eval = float("inf")

            for mov in movimientos:
                nuevo_tablero = tablero.copiar_tablero()

                nuevo_tablero.mover_pieza(mov[0], mov[1])
                nuevo_tablero.cambiar_turno()

                eval, _ = self.minimax_ab(nuevo_tablero, profundidad - 1, alpha, beta, True)

                if eval < min_eval:
                    min_eval, mejor_mov = eval, mov
                
                beta = min(beta, eval)
                if beta < alpha:
                    return (min_eval, mejor_mov)
            
            return (min_eval, mejor_mov)
    
    # ---------------------------------- FUNCIONES DE EVALUACIÓN ----------------------------------------------- #

    #Ventaja de Material Puro. Cada pieza tiene asociado un peso.
    def func_material_eval(self, tablero):
        #Revisión Estado Final. Retorna máxima o mínima puntuación (1e6).
        puntuación_final = self.estado_terminal(tablero)
        if puntuación_final is not None:
            return puntuación_final
        
        puntuacion = 0.0

        for fila in tablero.casillas:
            for pieza in fila:
                if pieza:
                    if pieza.color == self.color:
                        puntuacion += pieza.valor
                    else:
                        puntuacion -= pieza.valor
        
        return puntuacion

    #Ventaja de Material Reducida y Control del Centro.
    def func_centro_eval(self, tablero):

        puntuación_final = self.estado_terminal(tablero)
        if puntuación_final is not None:
            return puntuación_final

        W_MATERIAL = 0.4
        puntuacion = W_MATERIAL * self.func_material_eval(tablero)

        #Centro Tablero Variante Los Alamos (6x6, Centro 2x2).
        W_CCONTROL = 1.6
        CENTRO = [(2, 2), (2, 3), (3, 2), (3, 3)]
        for x, y in CENTRO:
            if tablero.filas > x >= 0.0 and tablero.columnas > y >= 0.0:
                pieza = tablero.casillas[x][y]
                if pieza:
                    if pieza.color == self.color:
                        puntuacion += W_CCONTROL
                    else:
                        puntuacion -= W_CCONTROL

        return puntuacion

    #Rey dinámico. Fase de juego media -> Rey escondido y seguro. Fase final -> Rey proactivo buscando el centro.
    def func_rey_eval(self, tablero):
        
        puntuacion_final = self.estado_terminal(tablero)
        if puntuacion_final is not None:
            return puntuacion_final
        
    
        puntuacion = 0.0
        W_FFINAL = 1.0
        W_FMEDIA = 0.7

        '''
            PEÓN : 1 x 6
            TORRE : 5 x 2
            CABALLO: 6 x 2
            DAMA : 9 x 1
            TOTAL: 31 por bando.
            
            62 TOTAL en partida.
            Juego final -> 20% material total restante: 0.2 x 62 : 12.4

        '''
        UMBRAL = 12.4

        #Material total SIN REYES.
        material = 0.0
        for fila in tablero.casillas:
            for pieza in fila:
                if pieza and not isinstance(pieza, Rey):
                    material += pieza.valor
            
        fase_juego = "final" if material <= UMBRAL else "medio"

        for x in range(tablero.filas):
            for y in range(tablero.columnas):
                pieza = tablero.casillas[x][y]
                if pieza and isinstance(pieza, Rey):
                    rey_centro = (3 >= x >= 2) and (3 >= y >= 2)
                    rey_esquina = (x == 0 or x == 5) or (y == 0 or y == 5)

                    #Posición Fuerte.
                    rey_ok = (fase_juego == "media" and rey_esquina) or (fase_juego == "final" and rey_centro)
                    #Posición Débil.
                    rey_nok = (fase_juego == "media" and rey_centro) or (fase_juego == "final" and rey_esquina)

                    W_REY = W_FFINAL if fase_juego == "final" else W_FMEDIA

                    if pieza.color == self.color:
                        if rey_ok:
                            puntuacion += W_REY
                        elif rey_nok:
                            puntuacion -= W_REY
                    else:
                        if rey_ok:
                            puntuacion -= W_REY
                        elif rey_nok:
                            puntuacion += W_REY

        #Control del Centro como añadido. Posición por encima de material puro.
        return puntuacion + self.func_centro_eval(tablero)    
