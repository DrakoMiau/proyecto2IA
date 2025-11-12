# no se si vayamos a integrar gui, pero aqui se podria juntar todo (?

from tablero import Tablero, Pieza, Peon, Caballo, Alfil, Reina, Rey, Torre

if __name__ == "__main__":
    t = Tablero()
    caballo = Caballo("blanco")
    t.colocar_pieza(1, 1, caballo)
    t.mostrar()

    print("\nMovimientos legales del caballo en (3,3):")
    print(caballo.movimientos_legales(t, 1,1))
