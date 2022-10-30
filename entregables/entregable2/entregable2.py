#!/usr/bin/env python3
import sys
from typing import TextIO

# Folleto en inglés es Leaflet
Leaflet = tuple[int, int, int]          # (num_folleto, anchura, altura)
LeafletPos = tuple[int, int, int, int]  # (num_folleto, num_hoja_de_imprenta, pos_x ,pos_y)
Hueco = list[int, int, int, int]  # x0 #x1 #y0 #y1

# Lee la instancia por la entrada estándar (ver apartado 1.1)
# Devuelve el tamaño del papel de la imprenta y la lista de folletos
def read_data(f: TextIO) -> tuple[int, list[Leaflet]]:
    tam: int = int(f.readline())
    lista: list[Leaflet] = []
    for line in f.readlines():
        cadena: list[str] = line.split(" ")
        tupla: tuple[int, int, int] = (int(cadena[0]), int(cadena[1]), int(cadena[2]))
        lista.append(tupla)

    return (tam, lista)



# Recibe el tamaño del papel de la imprenta y la lista de folletos
# Devuelve tamaño del papel y lista de folletos

def anyadir_folleto(hueco: Hueco, list_hojas: list[Hueco], hoja: int, resultado: list[LeafletPos], folleto: Leaflet):
    resultado.append((folleto[0], hoja + 1, hueco[0], hueco[2]))
    x = hueco[0] + folleto[1]
    y = hueco[2] + folleto[2]
    if x != hueco[1] and y != hueco[3]:  # si sobra hueco en el eje x o y del hueco despues de haber insertado el folleto
        if (hueco[1] - x) * (hueco[3] - hueco[2]) > (x - hueco[0]) * (hueco[3] - y):  # se divide la superficie sobrante verticalmente en 2 rectangulos y solo se añade el mas grande de ellos
            list_hojas[hoja] = [x, hueco[1], hueco[2], hueco[3]]
        else:
            list_hojas[hoja] = [hueco[0], x, y, hueco[3]]
    else:
        if x == hueco[1]:  # si no sobra hueco en x o en x e y
            hueco[2] = y
        else:
            hueco[0] = x  # si no sobra solo en y

def process(paper_size: int, leaflet_list: list[Leaflet]) -> list[LeafletPos]:
    #Creamos lista de tamaños de los folletos
    lista_tam = []
    for i in range(len(leaflet_list)):
        folleto = leaflet_list[i]
        lista_tam.append(folleto[1])
    indices = range(len(lista_tam))

    #Ordenamos de mayor a menor los folletos por anchura
    sorted_indices = sorted(indices, key=lambda i: -lista_tam[i])

    resultado: list[LeafletPos] = []
    list_hojas: list[Hueco] = [[0, paper_size, 0, paper_size]]
    sorted_indices_hojas: list[int] = [0]

    #Recorremos los folletos ordenados por superficie total
    for i in sorted_indices:
        folleto: Leaflet = leaflet_list[i]
        encajado = False
        for hoja in sorted_indices_hojas:  #recorremos las hojas en busca de un hueco para el folleto
            hueco = list_hojas[hoja]     #elegimos el hueco que hay en la hoja, ese hueco sera el hueco mas grande que la hoja tenia
            anchura = hueco[1] - hueco[0]
            altura = hueco[3] - hueco[2]
            if anchura >= folleto[1] and altura >= folleto[2]:
                encajado = True
                anyadir_folleto(hueco, list_hojas, hoja, resultado, folleto)
                break

        if not encajado: #si el hueco no es suficientemente grande creamos una nueva hoja hoja con un hueco con superficie total de la hoja
            hueco = [0, paper_size, 0, paper_size]
            list_hojas.append(hueco)
            sorted_indices_hojas.insert(0,len(list_hojas)-1) #para optimizar tiempo añadimos la hoja al principio de la lista de hojas
            anyadir_folleto(hueco, list_hojas, len(list_hojas) - 1, resultado, folleto)

    return resultado

# Muestra por la salida estandar las posiciones de los folletos (ver apartado 1.2)
def show_results(leafletpos_list: list[LeafletPos]):
    for linea in leafletpos_list:
        print(linea[0], " ", linea[1], " ", linea[2], " ", linea[3])


if __name__ == '__main__':
    paper_size0, leaflet_list0 = read_data(sys.stdin)
    leafletpos_list0 = process(paper_size0, leaflet_list0)
    show_results(leafletpos_list0)
