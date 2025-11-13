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

        # promocion de peon
        if isinstance(pieza, Peon):
            if (pieza.color == "blanco" and destino[0] == 0) or (pieza.color == "negro" and destino[0] == self.filas - 1):
                self.promocionar_peon(destino, pieza.color)


    def mostrar(self):
        for i, fila in enumerate(self.casillas):
            fila = self.casillas[i]
            print(f"{i} " + " ".join(". " if x is None else x.simbolo for x in fila))
        print("  " + " ".join(str(j) for j in range(self.columnas)))


    def cambiar_turno(self):
        self.turno_actual = "blanco" if self.turno_actual == "negro" else "negro"

    def limpiar_tablero(self):
        self.casillas = self.crear_tablero_vacio()

    def copiar_tablero(self):
        nuevo = Tablero(self.filas, self.columnas)
        nuevo.casillas = [fila[:] for fila in self.casillas]
        nuevo.turno_actual = self.turno_actual
        return nuevo

    def esta_en_jaque(self, color: str) -> bool:
            # 1. localizar el rey
            rey_pos = None
            for f in range(self.filas):
                for c in range(self.columnas):
                    pieza = self.casillas[f][c]
                    if pieza and isinstance(pieza, Rey) and pieza.color == color:
                        rey_pos = (f, c)
                        break
                if rey_pos:
                    break
            
            if not rey_pos:
                return False  # no hay rey (raro, pero evita errores)

            # 2. revisar si alguna pieza enemiga puede atacar esa posición
            enemigo = "negro" if color == "blanco" else "blanco"
            for f in range(self.filas):
                for c in range(self.columnas):
                    pieza = self.casillas[f][c]
                    if pieza and pieza.color == enemigo:
                        movimientos = pieza.movimientos_posibles(self, f, c)
                        if rey_pos in movimientos:
                            return True  # está en jaque
            return False
    

    def movimientos_legales(self, fila: int, columna: int):
        pieza = self.casillas[fila][columna]
        if not pieza:
            return []

        movimientos_legales = []
        for destino in pieza.movimientos_posibles(self, fila, columna):
            tablero_simulado = self.copiar_tablero()
            tablero_simulado.mover_pieza((fila, columna), destino)

            if not tablero_simulado.esta_en_jaque(pieza.color):
                movimientos_legales.append(destino)

        return movimientos_legales


    def promocionar_peon(self, posicion, color, nueva_pieza=None):
        """
        Promociona un peón en la posición dada.
        Si no se especifica una nueva pieza, se promueve a Reina por defecto.
        """
        fila, columna = posicion
        print(f"Promocionando peón {color} en ({fila},{columna})")

        if nueva_pieza is None:
            nueva_pieza = Reina(color)

        self.casillas[fila][columna] = nueva_pieza

    
    def hay_movimientos_legales(self, color: str) -> bool:
        """Retorna True si el jugador tiene al menos un movimiento legal."""
        for f in range(self.filas):
            for c in range(self.columnas):
                pieza = self.casillas[f][c]
                if pieza and pieza.color == color:
                    if self.movimientos_legales(f, c):  # ya los filtra contra jaque
                        return True
        return False


    def estado_del_juego(self) -> str:
        # esta funcion la empleo en el archivo juego.py para controlar el flujo
        color = self.turno_actual
        en_jaque = self.esta_en_jaque(color)
        hay_movs = self.hay_movimientos_legales(color)

        if en_jaque and not hay_movs:
            return "jaque_mate"
        elif not en_jaque and not hay_movs:
            return "tablas"
        elif en_jaque:
            return "jaque"
        else:
            return "en_juego"


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
    
    def movimientos_posibles(self, tablero, fila, columna): # deberia devolver tuplas de (pieza, (movimientos legales))
        return []

# prefiero subclases de cada para abrir un poco mas las posibilidades
# seria mas faci crear cosas para poder utilizarlas en las heuristicas
# primero por cada pieza la funcion movimientos legales

class Peon(Pieza):
    def __init__(self, color):
        simbolo = "Pb" if color == "blanco" else "Pn"
        super().__init__(color, simbolo, 1)

    def movimientos_posibles(self, tablero: Tablero, fila: int, columna: int):
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

    def movimientos_posibles(self, tablero: Tablero, fila:int, columna: int):
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

    def movimientos_posibles(self, tablero: Tablero, fila: int, columna: int):
        movimientos = []
        # logica del alfil
        direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # diagonales

        for df, dc in direcciones:
            nueva_fila, nueva_columna = fila + df, columna + dc

            while Utils.dentro_de_limites(nueva_fila, nueva_columna, tablero.filas, tablero.columnas):
                if not Utils.hay_pieza(tablero, nueva_fila, nueva_columna):
                    movimientos.append((nueva_fila, nueva_columna))
                else:
                    color_objetivo = Utils.color_de_pieza(tablero, nueva_fila, nueva_columna)
                    if color_objetivo != self.color:
                        movimientos.append((nueva_fila, nueva_columna))
                    break  # no puede saltar piezas
                nueva_fila += df
                nueva_columna += dc
        return movimientos

class Torre(Pieza):
    def __init__(self, color):
        simbolo = "Tb" if color == "blanco" else "Tn"
        super().__init__(color, simbolo, 5)

    def movimientos_posibles(self, tablero: Tablero, fila: int, columna: int):
        movimientos = []
        # logica de la torre
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izquierda, derecha

        for df, dc in direcciones:
            nueva_fila, nueva_columna = fila + df, columna + dc

            while Utils.dentro_de_limites(nueva_fila, nueva_columna, tablero.filas, tablero.columnas):
                if not Utils.hay_pieza(tablero, nueva_fila, nueva_columna):
                    movimientos.append((nueva_fila, nueva_columna))
                else:
                    color_objetivo = Utils.color_de_pieza(tablero, nueva_fila, nueva_columna)
                    if color_objetivo != self.color:
                        movimientos.append((nueva_fila, nueva_columna))
                    break
                nueva_fila += df
                nueva_columna += dc
        return movimientos


class Reina(Pieza):
    def __init__(self, color):
        simbolo = "Rb" if color == "blanco" else "Rn"
        super().__init__(color, simbolo, 9)

    def movimientos_posibles(self, tablero: Tablero, fila: int, columna: int):
        movimientos = []
        # lgica de la reina
        # combina direcciones de alfil y torre
        direcciones = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # torre
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # alfil
        ]

        for df, dc in direcciones:
            nueva_fila, nueva_columna = fila + df, columna + dc

            while Utils.dentro_de_limites(nueva_fila, nueva_columna, tablero.filas, tablero.columnas):
                if not Utils.hay_pieza(tablero, nueva_fila, nueva_columna):
                    movimientos.append((nueva_fila, nueva_columna))
                else:
                    color_objetivo = Utils.color_de_pieza(tablero, nueva_fila, nueva_columna)
                    if color_objetivo != self.color:
                        movimientos.append((nueva_fila, nueva_columna))
                    break  # no puede saltar
                nueva_fila += df
                nueva_columna += dc
        return movimientos


class Rey(Pieza):
    def __init__(self, color):
        simbolo = "Kb" if color == "blanco" else "Kn"
        super().__init__(color, simbolo, 1000)  #obvio es la pieza que mas vale

    def movimientos_posibles(self, tablero: Tablero, fila: int, columna: int):
        movimientos = []
        # logica del rey        
        # todas las direcciones posibles (8 alrededor)
        direcciones = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        for df, dc in direcciones:
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



if __name__ == "__main__":
    t = Tablero()
    t.limpiar_tablero()

    # Peón blanco cerca de la promoción
    t.colocar_pieza(1, 2, Peon("blanco"))
    t.mostrar()
    print("\n--- Movemos el peón blanco a la fila 0 ---")
    t.mover_pieza((1, 2), (0, 2))
    t.mostrar()

    print("\n--- PRUEBA DE PROMOCIÓN DE PEÓN NEGRO ---")
    t.limpiar_tablero()
    # Peón negro cerca de la promoción
    t.colocar_pieza(4, 3, Peon("negro"))
    t.mostrar()

    print("\n--- Movemos el peón negro a la fila 5 ---")
    t.mover_pieza((4, 3), (5, 3))
    t.mostrar()


