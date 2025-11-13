#aqui vamos a coordinar las demas clases para el flujo de la partida

from tablero import Tablero, Rey, Torre, Reina, Peon, Alfil, Caballo

class Juego:
    def __init__(self):
        self.tablero = Tablero()
        self.tablero.los_alamos_default()
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
            print(f"⚠️  {self.tablero.turno_actual} está en jaque.")

    def turno(self, origen, destino):
        """Ejecuta un turno completo."""
        if not self.en_juego:
            print("El juego ha terminado.")
            return

        self.tablero.mover_pieza(origen, destino)
        self.verificar_estado()

        if self.en_juego:
            self.tablero.cambiar_turno()
            print(f"Turno de {self.tablero.turno_actual}")



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
