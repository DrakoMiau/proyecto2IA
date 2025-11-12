# aqui vamos a definir el estado del juego, generar los movimientos posibles, validarlos y aplicarlos

from __future__ import annotations
from utils import Utils

class Tablero:
    def __init__(self, filas=6, columnas=6): # por defecto es el tablero 6x6
        self.turno_actual = "blanco"
        self.filas = filas
        self.columnas = columnas
        self.es_ajedrez_clasico = False
        self.casillas = self.crear_tablero_vacio()

    
    def crear_tablero_vacio(self):
        return [[None for _ in range(self.columnas)] for _ in range(self.filas)]
    
    def colocar_pieza(self, fila, columna, pieza: Pieza):
        #emplear cuando programe promocion de piezas, reiniciar o crear un tablero
        #tal vez si quiero crear variantes
        self.casillas[fila][columna] = pieza

    def mover_pieza(self, origen, destino): #se reciben dos tuplas como una tupla
        #tengo que verificar si hay una pieza existente en esa casilla
        #luego ver si el movimiento que quiero realizar esta dentro de movimientos posibles
        pieza = self.casillas[origen[0]][origen[1]]
        if pieza is None:
            print("no hay pieza para mover")
            return
        self.casillas[origen[0]][origen[1]] = None
        self.casillas[destino[0]][destino[1]] = pieza


    def mostrar(self):
        for i, fila in enumerate(self.casillas):
            fila = self.casillas[i]
            print(f"{i} " + " ".join("." if x is None else x.simbolo for x in fila))
        print("  " + " ".join(str(j) for j in range(self.columnas)))


    def cambiar_turno(self):
        self.turno_actual = "blanco" if self.turno_actual == "negro" else "negro"

    def limpiarTablero(self):
        self.casillas = self.crear_tablero_vacio()


    #algunas disposiciones, si quieren agregar alguna otra, bien puedan

    def los_alamos_default(self):
        if self.filas != 6 or self.columnas != 6: 
            return #poner algun error de que el tablero no se puede crear para estas dimensiones
        
        self.casillas = self.crear_tablero_vacio()
        # negras
        self.colocar_pieza(0, 0, Torre("negro"))
        self.colocar_pieza(0, 1, Caballo("negro"))
        self.colocar_pieza(0, 2, Reina("negro"))
        self.colocar_pieza(0, 3, Rey("negro"))
        self.colocar_pieza(0, 4, Caballo("negro"))
        self.colocar_pieza(0, 5, Torre("negro"))
        for x in range(6):
            self.colocar_pieza(1, x, Peon("negro"))

        # blancas
        self.colocar_pieza(5, 0, Torre("blanco"))
        self.colocar_pieza(5, 1, Caballo("blanco"))
        self.colocar_pieza(5, 2, Reina("blanco"))
        self.colocar_pieza(5, 3, Rey("blanco"))
        self.colocar_pieza(5, 4, Caballo("blanco"))
        self.colocar_pieza(5, 5, Torre("blanco"))
        for x in range(6):
            self.colocar_pieza(4, x, Peon("blanco"))




class Pieza:
    #vamos a utilizar claramente valor como heuristica, toca ir pensando en que otra es vaida
    #por ej como podemos cuantificar la posicion, porque en algunos casos, es importante esquinear el rey
    #sin embargo, cuando quedan pocas piezas sobre el tablero, es importante centrar el rey para utilizarlo
    def __init__(self, color, simbolo, valor):
        self.color = color
        self.simbolo = simbolo
        self.valor = valor
    
    def movimientos_posibles(self, tablero, fila, columna):
        return []

# prefiero subclases de cada para abrir un poco mas las posibilidades
# seria mas faci crear cosas para poder utilizarlas en las heuristicas
# primero por cada pieza la funcion movimientos legales

class Peon(Pieza):
    def __init__(self, color):
        simbolo = "Pb" if color == "blanco" else "Pn"
        super().__init__(color, simbolo, 1)

    def movimientos_legales(self, tablero: Tablero, fila: int, columna: int):
        movimientos = []
        #meter logica
        #direccion de avance segun el color
        direccion = -1 if self.color == "blanco" else 1

        # movimiento hacia adelante
        nueva_fila = fila + direccion
        nueva_columna = columna

        if Utils.dentro_de_limites(nueva_fila, nueva_columna, tablero.filas, tablero.columnas):
            if not Utils.hay_pieza(tablero, nueva_fila, nueva_columna):
                movimientos.append((nueva_fila, nueva_columna))

        # capturas en diagonales
        for desplazamiento_columna in [-1, 1]:
            nueva_fila = fila + direccion
            nueva_columna = columna + desplazamiento_columna

            if Utils.dentro_de_limites(nueva_fila, nueva_columna, tablero.filas, tablero.columnas):
                if Utils.hay_pieza(tablero, nueva_fila, nueva_columna):
                    if Utils.color_de_pieza(tablero, nueva_fila, nueva_columna) != self.color:
                        movimientos.append((nueva_fila, nueva_columna))

        # agregar el doble movimiento del peon, considerar el atributo que determina si es clasico o no
        return movimientos


class Caballo(Pieza):
    def __init__(self, color):
        simbolo = "Cb" if color == "blanco" else "Cn"
        super().__init__(color, simbolo, 3)

    def movimientos_legales(self, tablero: Tablero, fila:int, columna: int):
        movimientos = []
        # logica del caballo
        desplazamientos = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1),
        ]

        if not Utils.hay_pieza(tablero, fila, columna):
            print("No hay ninguna pieza en esta posición.")
            return []
        elif not isinstance(tablero.casillas[fila][columna], Caballo):
            print("La pieza en esta posición no es un Caballo.")
            return []
        for df, dc in desplazamientos:
            nueva_fila = fila + df
            nueva_columna = columna + dc

            if Utils.dentro_de_limites(nueva_fila, nueva_columna, tablero.filas, tablero.columnas):
                if not Utils.hay_pieza(tablero, nueva_fila, nueva_columna):
                    movimientos.append((nueva_fila, nueva_columna))
                else:
                    color_objetivo = Utils.color_de_pieza(tablero, nueva_fila, nueva_columna)
                    if color_objetivo != self.color:
                        movimientos.append((nueva_fila, nueva_columna))
        
        return movimientos


class Alfil(Pieza):
    def __init__(self, color):
        simbolo = "Ab" if color == "blanco" else "An"
        super().__init__(color, simbolo, 3)

    def movimientos_legales(self, tablero: Tablero, fila: int, columna: int):
        movimientos = []
        # logica del alfil
        return movimientos

class Torre(Pieza):
    def __init__(self, color):
        simbolo = "Tb" if color == "blanco" else "Tn"
        super().__init__(color, simbolo, 5)

    def movimientos_legales(self, tablero: Tablero, fila: int, columna: int):
        movimientos = []
        # logica de la torre
        return movimientos


class Reina(Pieza):
    def __init__(self, color):
        simbolo = "Rb" if color == "blanco" else "Rn"
        super().__init__(color, simbolo, 9)

    def movimientos_legales(self, tablero: Tablero, fila: int, columna: int):
        movimientos = []
        # lgica de la reina
        return movimientos


class Rey(Pieza):
    def __init__(self, color):
        simbolo = "Kb" if color == "blanco" else "Kn"
        super().__init__(color, simbolo, 1000)  #obvio es la pieza que mas vale

    def movimientos_legales(self, tablero: Tablero, fila: int, columna: int):
        movimientos = []
        # logica del rey
        return movimientos


if __name__ == "__main__":
    t = Tablero()
    t.colocar_pieza(1, 1, Peon("blanco"))
    t.colocar_pieza(4, 2, Caballo("negro"))

    print("posiciones iniciales")
    t.mostrar()

    t.mover_pieza((1, 1), (2, 1))
    print("\nmovemos un peoncito")
    t.mostrar()

    print("\n ahora una configuracion completa de los alamos chess por defecto")
    t.los_alamos_default()
    t.mostrar()

    movimientos_peon = t.casillas[4][1].movimientos_legales(t, 4, 1)
    color_peon = Utils.color_de_pieza(t, 4, 1)
    print(movimientos_peon)
    print(color_peon)

    t.mover_pieza((4,1), (3,1))
    t.mover_pieza((1,2), (2,2))
    t.mostrar()

    movimientos_peon_blanco = t.casillas[3][1].movimientos_legales(t,3,1)
    print(movimientos_peon_blanco)
    movimientos_peon_negro = t.casillas[2][2].movimientos_legales(t,2,2)
    print(movimientos_peon_negro)


