from __future__ import annotations
from tablero import Tablero, Pieza

class Utils:
    @staticmethod
    def dentro_de_limites(fila: int, columna: int, total_filas: int, total_columnas: int):
        return 0 <= fila < total_filas and 0 <= columna < total_columnas

    @staticmethod
    def hay_pieza(tablero: Tablero, fila: int, columna: int):
        if tablero.casillas[fila][columna] != None:
            return True
        else:
            return False

    @staticmethod
    def color_de_pieza(tablero: Tablero, fila: int, columna: int):
        pieza = tablero.casillas[fila][columna]  
        if pieza:
            return pieza.color
        else:
            return None

    @staticmethod
    def obtener_todos_movimientos(tablero, color):
        movimientos = []
        
        for x in range(tablero.filas):
            for y in range(tablero.columnas):
                pieza = tablero.casillas[x][y]
                if pieza and pieza.color == color:
                    movimientos_posibles = tablero.movimientos_legales(x, y)
                    origen = (x, y)
                    for destino in movimientos_posibles:
                        movimientos.append((origen, destino))
                        
        return movimientos
    
    @staticmethod
    def test_movimientos(tablero: Tablero, fila: int, columna: int):
        pieza = tablero.casillas[fila][columna]
        if pieza is None:
            print(f"si no hay pieza en ({fila}, {columna})")
            return

        print(f"\nProbando movimientos de {pieza.simbolo} en posición ({fila}, {columna})")
        movimientos = pieza.movimientos_posibles(tablero, fila, columna)

        #creamos un tablero temporal para mostrar los movimientos
        tablero_temporal = Tablero(tablero.filas, tablero.columnas)
        tablero_temporal.casillas = [fila[:] for fila in tablero.casillas]

        # marcar los movimientos posibles con un símbolo especial temporal
        for (f, c) in movimientos:
            if tablero_temporal.casillas[f][c] is None:
                # casillas a las que puede saltar sin comer
                tablero_temporal.casillas[f][c] = Pieza("marca", "xx", 0)
            else:
                # pueza enemiga y puede comer
                tablero_temporal.casillas[f][c].simbolo = "XX"
        
        tablero_temporal.mostrar()
        print(f'movimientos legales {movimientos}')
