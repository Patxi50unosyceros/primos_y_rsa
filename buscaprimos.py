#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from datetime import datetime as t
from json import dump as guardar
from json import load as cargar
import os.path as ruta


# crea un archivo llamado NOMBRE_ARCHIVO con todos los números primos
# entre 2 y LIMITE , haciendo un guardado automatico cada 30 segundos
# y reanudando el trabajo donde lo dejó si se interrumpe el proceso.


limite = 99999999  # 4294967296 = 32 bits = 4 bytes por numero
relojes = [t.now(), 30]
nombre_archivo = 'listpri.txt'


def ha_pasao_segs(relojes):
    if (t.now()-relojes[0]).seconds > relojes[1]:
        relojes[0] = t.now()
        return True
    else:
        return False


def es_primo(numero, primos, relojes, nombre_archivo):
    if ha_pasao_segs(relojes):
        print(str(t.now().strftime('%H:%M:%S')) + " probando: " + str(numero) + " _ ultimos p: " + str(primos[-3:-1]))
        with open(nombre_archivo, 'w') as archivo:
            guardar(primos, archivo)
    divisor_limite = math.isqrt(numero)+2
    for divisor in primos:
        if divisor < divisor_limite:
            if numero % divisor == 0:
                return False
        else:
            break
    return True


def intentar_recuperar_ultimo_guardado(nombre_archivo):
    # primero mirar si existe el archivo
    if ruta.exists(nombre_archivo):
        # si existe el archivo lo leemos...
        primos_encontrados = []
        with open(nombre_archivo, 'r') as archivo:
            primos = cargar(archivo)
            primos_encontrados += primos
            ultimo_primo = primos[-1]
        return [ultimo_primo, primos_encontrados]
    else:
        return [9, [3, 5, 7]]


# intentando cargar datos
respuesta = intentar_recuperar_ultimo_guardado(nombre_archivo)
primos = respuesta[1]
actual = respuesta[0]

print("RecopilandoPrimos\n...empezando por: " + str(actual) + " a las " + str(t.now().strftime('%H:%M:%S')))


while actual < limite:
    if es_primo(actual, primos, relojes, nombre_archivo):
        primos.append(actual)
    actual += 2

# guardando
print(str(t.now().strftime('%H:%M:%S')) + " guardado final...")
with open(nombre_archivo, 'w') as archivo:
    guardar(primos, archivo)

# salida
print("\nFin de Programa al llegar a " + str(limite))
print(primos[-5:-1])
