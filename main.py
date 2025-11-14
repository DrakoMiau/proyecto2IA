# no se si vayamos a integrar gui, pero aqui se podria juntar todo (?

from tablero import Tablero, Pieza, Peon, Caballo
from jugador import Jugador

def test_movimientos(tablero: Tablero, fila: int, columna: int):
    pieza = tablero.casillas[fila][columna]
    if pieza is None:
        print(f"No hay pieza en ({fila}, {columna})")
        return

    print(f"\nProbando movimientos de {pieza.simbolo} en posición ({fila}, {columna})")
    movimientos = pieza.movimientos_posibles(tablero, fila, columna)

    # crear una copia del tablero para mostrar los movimientos
    tablero_temporal = Tablero(tablero.filas, tablero.columnas)
    tablero_temporal.casillas = [fila[:] for fila in tablero.casillas]

    # marcar los movimientos posibles con un símbolo especial temporal
    for (f, c) in movimientos:
        if tablero_temporal.casillas[f][c] is None:
            # marcar con un punto de destino
            tablero_temporal.casillas[f][c] = Pieza("marca", "xx", 0)
        else:
            # si hay una pieza enemiga, marcar con una X mayúscula
            tablero_temporal.casillas[f][c].simbolo = "XX"

    tablero_temporal.mostrar()
    print(f"Movimientos legales: {movimientos}")


if __name__ == "__main__":
    #PRINCIPAL
    '''
        Modalidad: Los Alamos (6x6)

        Reglas:
            - Tablero 6x6
            - No movimiento doble inicial de Peones
            - No <<En Passant>>
            - No Alfíles (Bishops)

        Configuración Inicial:

                    T C D R C T
                    P P P P P P


                    P P P P P P
                    T C D R C T

            Peon (P), Torre (T), Caballo (C), Dama (D), Rey (R)

        *Representación interna varía. Nombres en español con fines ilustrativos.
        ** Inician blancas.
    '''

    # --------------------------- SETUP -------------------------------- #

    #TABLERO
    tablero = Tablero()
    tablero.los_alamos_default()

    #AGENTES
    IA_Negra  = Jugador(color = "negro", profundidad = 3, func_eval = "rey")
    IA_Blanca = Jugador(color = "blanco", profundidad = 3, func_eval = "centro")

    #Inician blancas
    jugador_actual = IA_Blanca

    # ----------------------- BUCLE PRINCIPAL ---------------------------- #

    tablero.mostrar()

    while True:
        
        jugador_actual = IA_Blanca if tablero.turno_actual == "blanco" else IA_Negra

        mejor_mov = jugador_actual.obtener_mejor_movimiento(tablero)
        if mejor_mov is None:
            print("gg manco")
            break

        #Origen, Destino
        tablero.mover_pieza(mejor_mov[0], mejor_mov[1])

        tablero.cambiar_turno()
        
        tablero.mostrar()
    
    # ------------------------------- FINAL ------------------------------------------ #

    estado_final = tablero.estado_del_juego()
    if estado_final == "jaque_mate":
        ganador = "blanco" if tablero.turno_actual == "negro" else "negro"
        print(f"gg. Ganador: {ganador}\n")
    elif estado_final == "tablas":
        print(f"gg. Malos los dos. Empate.\n")