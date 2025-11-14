#aqui vamos a coordinar las demas clases para el flujo de la partida

from tablero import Tablero, Rey, Torre, Reina, Peon, Alfil, Caballo
from jugador import Jugador

class Juego:
    
    def __init__(self, d_blanca = 3, feval_blanca = "centro", d_negra = 3, feval_negra = "rey"):
        self.tablero = Tablero()
        self.tablero.los_alamos_default()

        #AGENTES
        self.IA_Negra  = Jugador(color = "negro", profundidad = d_negra, func_eval = feval_negra)
        self.IA_Blanca = Jugador(color = "blanco", profundidad = d_blanca, func_eval = feval_blanca)

        #Inician blancas
        self.jugador_actual = self.IA_Blanca
        self.en_juego = True


    def verificar_estado(self):
        estado = self.tablero.estado_del_juego()

        if estado == "jaque_mate":
            ganador = "blanco" if self.tablero.turno_actual == "negro" else "negro"
            print(f"¡Jaque mate! Ganan las {ganador}s.")
            self.en_juego = False

        elif estado == "tablas":
            print("Tablas. No hay movimientos posibles.")
            self.en_juego = False

        elif estado == "jaque":
            print(f"{self.tablero.turno_actual} está en jaque.")



    def game_loop(self):
        self.tablero.mostrar()

        while True:
        
            jugador_actual = self.IA_Blanca if self.tablero.turno_actual == "blanco" else self.IA_Negra

            mejor_mov = jugador_actual.obtener_mejor_movimiento(self.tablero)
            if mejor_mov is None:
                print("gg manco")
                break

            #Origen, Destino
            self.tablero.mover_pieza(mejor_mov[0], mejor_mov[1])

            self.tablero.cambiar_turno()
        
            self.tablero.mostrar()
    
        # ------------------------------- FINAL ------------------------------------------ #
        self.verificar_estado()
        #self.resultado_final()
    



if __name__ == "__main__":
    # ----- PRUEBA 1: JAQUE MATE DE PASILLO -----
    print("\n=== PRUEBA 1: JAQUE MATE DE PASILLO ===")
    juego = Juego()
    t = juego.tablero
    t.limpiar_tablero()  # aseguramos tablero vacío
    print(t.turno_actual)

    # colocar piezas
    t.colocar_pieza(5, 5, Rey("blanco"))
    t.colocar_pieza(4, 5, Peon("blanco"))
    t.colocar_pieza(4, 4, Peon("blanco"))
    t.colocar_pieza(4, 3, Peon("blanco"))
    t.colocar_pieza(5, 0, Torre("negro"))

    t.mostrar()
    print("\nEstado:", t.estado_del_juego())  # debería ser jaque mate

    # ----- PRUEBA 2: JAQUE MATE CON REY Y TORRE -----
    print("\n=== PRUEBA 2: JAQUE MATE CON REY Y TORRE ===")
    juego = Juego()
    t = juego.tablero
    t.limpiar_tablero()

    # rey encerrado xd
    t.colocar_pieza(0, 1, Rey("blanco"))
    # rey blanco ayuda
    t.colocar_pieza(2, 1, Rey("negro"))
    # torre da mate
    t.colocar_pieza(0, 5, Torre("negro"))

    t.mostrar()
    print("\nEstado:", t.estado_del_juego())  # debería ser jaque mate
