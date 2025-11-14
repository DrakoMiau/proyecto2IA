# no se si vayamos a integrar gui, pero aqui se podria juntar todo (?
import pyglet
from juego import Juego
from graficos import GUI

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
    '''
        Class Juego
        Parámetros:
        - Profundidad IA_Blanca
        - Función de Evaluación IA_Blanca
        - Profundidad IA_Negra
        - Función de Evaluación IA_Negra

        Funciones de Evaluación disponibles:
        - "material" : Ventaja pura de material
        - "centro" : Ventaja de material reducida y enfóque en el desarrollo central
        - "rey" : Rey dinámico según el estado de la partida. Estado final (tardío), prioriza el centro
                  Estado medio (mid), prioriza protegerse hacia las esquinas.
                  Un estado es tardío si el total de material en juego es LEQ 20% sin contar a los Reyes.
    '''
    
    GameInstance = Juego(d_blanca = 3, feval_blanca = "centro", d_negra = 3, feval_negra = "rey")
    #GameInstance.game_loop()
    GameGUI = GUI(juego = GameInstance)
    pyglet.app.run()