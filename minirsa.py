#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import dump as guardar
from json import load as cargar
import os.path as ruta
from random import randint as aleatorio


# este programa busca el archivo llamado 'listpri.txt' para leer de él
# la lista de números primos disponibles; se espera que el archivo contenga
# los 5.760.000 primeros números primos existentes (el generado por
# buscaprimos con el que busqué los números hasta 99999989
#
# tras cargar los primos disponibles escoge 2 al azar, y tras construir
# una pareja de claves, las aplica sobre un dato aleatorio.
#
# 
# Tras seleccionar primos y modulos...  Primos: 7740647 y 72373201
#                                       ModSec· 560215321087200
#                                       ModPub· 560215401201047
#
# Calculando Clave Publica [metodo clasico]...
#        Encontradas 5761451 Claves Publicas posibles...
#        ¡ Seleccionada como clave 47329231 !
#
# Calculando Clave Privada [metodo rapido]...
#        ¡ Seleccionada como clave 69598515969871
#
# PROBANDO A CIFRAR Y DESCIFRAR CON RSA
#        Claro^ClaPub = CIFRADO % modPub = Cifrado
#        Cifrado^ClaPri = CLARO % modPub = Claro
#
# 194471569792968 ^ 47329231 = algo %560215401201047 = 305559513094962
# 305559513094962 ^ 69598515969871 = algo %560215401201047 = 194471569792968
#
# ··· EXITO ···


def cargar_arch(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        return cargar(archivo)


def guardar_arch(diccionario_de_datos, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        guardar(diccionario_de_datos, archivo)


def cargar_primos():
    if ruta.exists('listpri.txt'):
        primos = []
        with open('listpri.txt', 'r') as archivo:
            lista_leida = cargar(archivo)
            primos += lista_leida
        print("\n" + str(len(primos)) + " números primos   ( último: " + str(primos[-1]) + " )")
        return primos
    else:
        print("\nArchivo de primos no encontrado... ")
        exit(0)


def elegir_primo(lista_primos, limite):
    if limite == 0:
        posicion = aleatorio(0, len(lista_primos)-1)
        return lista_primos[posicion]
    else:
        posicion = aleatorio(0, limite)
        return lista_primos[posicion]


def elegir_dos_primos(lista_primos, limite):
    a = elegir_primo(lista_primos, limite)
    b = a
    while b == a:
        b = elegir_primo(lista_primos, limite)
    return a, b


def calcular_modulos(primoA, primoB):
    modSec = (primoA - 1) * (primoB - 1)
    modPub = primoA * primoB
    return modSec, modPub


def calcular_clave_publica_classic(lista_primos, modSec):
    lista = []
    for primo in lista_primos:  # clave publica debe ser un primo
        if primo < modSec:  # clave publica debe ser inf a modSec
            if modSec % primo != 0:  # resto de modSec / primo != 0
                lista.append(primo)  # agregamos a lista candidatos
    print("\tEncontradas " + str(len(lista)) + " Claves Publicas posibles...")
    return lista[aleatorio(0, (len(lista) - 1))]  # elegido uno al azar


def calcular_privada_classic(claPub, modSec):
    for i in range(1, modSec):
        r = (claPub * i) % modSec
        if r == 1:
            print("\t" + str(claPub) + "x" + str(i) + " = " + str(claPub * i) + " mod " + str(modSec) + " = " + str(r))
            return i
    print("\t········· ERROR FATAL ·· CLAVE PRIVADA NO ENCONTRADA ····················")
    return 0


def hemos_creado_ultima_fila(tabla, claPub, modSec):
    ultima_fila = len(tabla)-1
    if abs(tabla[ultima_fila][2]) == abs(claPub) and abs(tabla[ultima_fila][3]) == abs(modSec):
        return True
    else:
        return False

    
def generar_nueva_fila(tabla):
    anteultima_fila = len(tabla)-2  # ............................... anteult : cociente_au resto_au u_au v_au
    ultima_fila = len(tabla)-1  # ...................................     ult : cociente_u  resto_u  u_u  v_u
    dividendo = tabla[anteultima_fila][1]  # ........................   NUEVA : cociente_N  resto_N  u_N  v_N
    divisor = tabla[ultima_fila][1]  # ................................
    cociente = int(dividendo / divisor)  # ............................ cociente_N = int( resto_au / resto_u )
    resto = int(dividendo % divisor)  # ...............................    resto_N = int( resto_au % resto_u )
    u = tabla[anteultima_fila][2]-(cociente*tabla[ultima_fila][2])  # .        u_N = u_au - (cociente_N * u_u)
    v = tabla[anteultima_fila][3]-(cociente*tabla[ultima_fila][3])  # .        v_N = v_au - (cociente_N * v_u)
    return [cociente, resto, u, v]


def extraer_inverso(tabla, modSec):
    anteultima_fila = len(tabla)-2
    numero = tabla[anteultima_fila][3]
    if numero > 0:
        return numero  # ................. si número > 0 => resultado = número
    else:
        return modSec + numero  # ........ si número < 0 => resultado = módulo + número ; ej: 32 + (-7) = 32-7 = 25


def calcular_privada_rapido(claPub, modSec):
    fila0 = [0, modSec, 1, 0]
    fila1 = [0, claPub, 0, 1]
    tabla = [fila0, fila1]
    while not hemos_creado_ultima_fila(tabla, claPub, modSec):
        tabla.append(generar_nueva_fila(tabla))
    return extraer_inverso(tabla, modSec)


def crear_valores_aleatorios(modPub, cantidad):
    lista = []
    while len(lista) < cantidad:
        nuevo = aleatorio(0, modPub-1)
        while nuevo in lista:
            nuevo = aleatorio(0, modPub - 1)
        lista.append(nuevo)
    return lista


def prueba_rsa_classic(modPub, claPub, claPri, prueba):
    valor_claro = prueba
    grande_cifrado = pow(valor_claro, claPub)
    valor_cifrado = grande_cifrado % modPub
    grande_claro = pow(valor_cifrado, claPri)
    valor_recuperado = grande_claro % modPub
    print(str(valor_claro)+'^'+str(claPub)+'=_tam'+str(len(str(grande_cifrado)))+'_%'+str(modPub)+'='+str(valor_cifrado))
    print(str(valor_cifrado)+'^'+str(claPri)+'=_tam'+str(len(str(grande_claro)))+'_%'+str(modPub)+'='+str(valor_recuperado))
    if valor_claro == valor_recuperado:
        print("··· EXITO ···\n")
    else:
        print("····································································· ERROR ············\n")
    return 0


def mi_exp_rap(base, exponente, modulo):
    exponente_en_binario_en_lista = list(str(format(exponente, "b")))  # base 7, exp 12 (1100), mod 80
    resultado = 1                                                      # ......... r = 1
    for valor_binario in exponente_en_binario_en_lista:                # e3=1  r = ( r^2 * b^e ) mod =   1*7 mod 80 = 7
        if int(valor_binario) == 1:                                    # e2=1  r = ( r^2 * b^e ) mod =  49*7 mod 80 = 23
            resultado = (resultado*resultado*base) % modulo            # e1=0  r = ( r^2 * b^e ) mod = 529*1 mod 80 = 49
        else:                                                          # e0=0  r = ( r^2 * b^e ) mod = 2041*1 mod 80 = 1
            resultado = (resultado*resultado) % modulo                 #
    return resultado                                                   # 7^12 mod 80 = 13.841.287.201 mod 80 = 1


def prueba_rsa_exp_rap(modPub, claPub, claPri, prueba):
    valor_claro = prueba
    valor_cifrado = mi_exp_rap(valor_claro, claPub, modPub)
    valor_recuperado = mi_exp_rap(valor_cifrado, claPri, modPub)
    print(str(valor_claro)+'^'+str(claPub)+'= algo %'+str(modPub)+'='+str(valor_cifrado))
    print(str(valor_cifrado)+'^'+str(claPri)+'= algo %'+str(modPub)+'='+str(valor_recuperado))
    if valor_claro==valor_recuperado:
        print("··· EXITO ···\n")
    else:
        print("····································································· ERROR ············\n")
    return 0


# -----------------------------------------------------------------------------------------------------------------
# Ejercicio Sobre RSA con PrimosPreCalculados

lista_primos = cargar_primos()  # cargando primos desde archivo... si no carga... FIN de ejercicio...

limite_pruebas = 5760000  # posicion máxima admisible en la lista de primos ( 5.761.457 primos = 99999989 )

primoA, primoB = elegir_dos_primos(lista_primos, limite_pruebas)
modSec, modPub = calcular_modulos(primoA, primoB)
print("\nTras seleccionar primos y modulos...")
print("Primos: " + str(primoA) + " y " + str(primoB) + "\nModSec· " + str(modSec) + "\nModPub· " + str(modPub))

print("\nCalculando Clave Publica [metodo clasico]...")
claPub = calcular_clave_publica_classic(lista_primos, modSec)
print("\t¡ Seleccionada como clave " + str(claPub) + " !")
claPri = 0
if limite_pruebas < 1000:
    print("\nCalculando Clave Privada [metodo clasico]...")
    claPri += calcular_privada_classic(claPub, modSec)
    print("\t¡ Seleccionada como clave " + str(claPri) + " !")
print("\nCalculando Clave Privada [metodo rapido]...")
claPri = calcular_privada_rapido(claPub, modSec)
print("\t¡ Seleccionada como clave " + str(claPri))

print("\n\nPROBANDO A CIFRAR Y DESCIFRAR CON RSA")
print('\tClaro^ClaPub = CIFRADO % modPub = Cifrado')
print('\tCifrado^ClaPri = CLARO % modPub = Claro\n')

lista_pruebas = crear_valores_aleatorios(modPub, 2)
if 80 > limite_pruebas > 0:  # ..................... modo lento... solo si primos peques
    for prueba in lista_pruebas:
        prueba_rsa_classic(modPub, claPub, claPri, prueba)
else:  # ........................................... modo rápido... exponenciacion rapida
    for prueba in lista_pruebas:
        prueba_rsa_exp_rap(modPub, claPub, claPri, prueba)

print("FIN EJERCICIO ········································ ")
# -----------------------------------------------------------------------------------------------------------------
