from __future__ import annotations

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
