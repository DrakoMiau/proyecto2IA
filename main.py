# no se si vayamos a integrar gui, pero aqui se podria juntar todo (?

from tablero import Tablero, Pieza, Peon, Caballo, Alfil, Reina, Rey, Torre


def test_movimientos(tablero: Tablero, fila: int, columna: int):
    pieza = tablero.casillas[fila][columna]
    if pieza is None:
        print(f"No hay pieza en ({fila}, {columna})")
        return

    print(f"\nProbando movimientos de {pieza.simbolo} en posición ({fila}, {columna})")
    movimientos = pieza.movimientos_legales(tablero, fila, columna)

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
    t = Tablero()
    '''
    caballo = Caballo("blanco")
    t.colocar_pieza(1, 1, caballo)
    t.mostrar()
    print("\nMovimientos legales del caballo en (3,3):")
    print(caballo.movimientos_legales(t, 1,1))
    '''
    t.limpiarTablero()
    #t.los_alamos_default()
    caballo = Caballo("blanco")
    peon = Peon("blanco")
    t.colocar_pieza(2, 2, peon)
    t.colocar_pieza(3, 4, caballo)
    test_movimientos(t, 3, 4)
