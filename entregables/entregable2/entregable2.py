#!/usr/bin/env python3
import sys
from typing import TextIO
from algoritmia.datastructures.priorityqueues import MinHeap

# Folleto en inglés es Leaflet
Leaflet = tuple[int, int, int]          # (num_folleto, anchura, altura)
LeafletPos = tuple[int, int, int, int]  # (num_folleto, num_hoja_de_imprenta, pos_x ,pos_y)


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
def process(paper_size: int, leaflet_list: list[Leaflet]) -> list[LeafletPos]:
    #Creamos lista de tamaños de los folletos
    lista_tam = []
    for i in range(len(leaflet_list)):
        folleto = leaflet_list[i]
        lista_tam.append(folleto[1] * folleto[2])
    indices = range(len(lista_tam))

    #Ordenamos de mayor a menor el tamaño de los folletos
    sorted_indices = sorted(indices, key=lambda i: -lista_tam[i])

    resultado: list[LeafletPos] = []
    hueco = list[int, int, int, int] #x0 #x1 #y0 #y1
    #dict_hojas: dict[int, hueco] = {1:[0, paper_size, 0, paper_size]}
    dict_hojas: list[hueco] = [[0, paper_size, 0, paper_size]]

    for i in sorted_indices:
        folleto: Leaflet = leaflet_list[i]
        #print(folleto)
        encajado = False
        #print(dict_hojas)
        for hoja in range(len(dict_hojas)):
            hueco = dict_hojas[hoja]
            anchura = hueco[1] - hueco[0]
            altura = hueco[3] - hueco[2]
            if anchura >= folleto[1] and altura >= folleto[2]:
                encajado = True
                resultado.append((folleto[0], hoja+1, hueco[0], hueco[2]))
                x = hueco[0] + folleto[1]
                y = hueco[2] + folleto[2]
                if  x != hueco[1] and y != hueco[3]:
                    if (hueco[1] - x)*(y-hueco[2]) > (hueco[1] - hueco[0])*(hueco[3] - y):
                        dict_hojas[hoja] = [x, hueco[1], hueco[2], y]
                        break
                    else:
                        dict_hojas[hoja]= [hueco[0], hueco[1], y, hueco[3]]
                if x == hueco[1]:
                    hueco[2] = y
                    break
                hueco[0] = x
                break
        if not encajado:
            hueco = [0, paper_size, 0, paper_size]
            dict_hojas.append(hueco)

            resultado.append((folleto[0], len(dict_hojas), hueco[0], hueco[2]))
            x = hueco[0] + folleto[1]
            y = hueco[2] + folleto[2]
            if (hueco[1] - x)*(y-hueco[2]) > (hueco[1] - hueco[0])*(hueco[3] - y):
                dict_hojas[len(dict_hojas)-1] = [x, hueco[1], hueco[2], y]
            else:
                dict_hojas[len(dict_hojas)-1] = [hueco[0], hueco[1], y, hueco[3]]

    return resultado

# Muestra por la salida estandar las posiciones de los folletos (ver apartado 1.2)
def show_results(leafletpos_list: list[LeafletPos]):
    for linea in leafletpos_list:
        print(linea[0], " ", linea[1], " ", linea[2], " ", linea[3])


if __name__ == '__main__':
    paper_size0, leaflet_list0 = read_data(sys.stdin)
    leafletpos_list0 = process(paper_size0, leaflet_list0)
    show_results(leafletpos_list0)
