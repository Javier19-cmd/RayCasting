"""
Referencia: 
1. Multiplicación de matrices:
    https://www.youtube.com/watch?v=IbzzK9PtFBE&ab_channel=ManuelGonzález

2. Suma de dos matrices:
    https://www.youtube.com/watch?v=CDozWggBP6Y&t=367s&ab_channel=ManuelGonzález
3. Importando la clase array:
    https://www.youtube.com/watch?v=6a39OjkCN5I&ab_channel=Telusko
"""
from array import *
class Matriz(object): #Clase para las matrices.

    def __init__(self, m: array): #Recibiendo como parámetro un array de números.
        self.m = m

    #Método para multiplicar dos matrices iguales.
    def __mul__(self, other): 
        if len(self.m[0]) == len(other.m): #Comprobamos que las matrices se puedan multiplicar.
            m3 = [] #Creamos una matriz vacía para el resultado.
            for i in range(len(self.m)): #Recorremos la matriz m1.
                m3.append([])
                for j in range(len(other.m[0])): #Recorremos la matriz m2.
                    m3[i].append(0) #Añadimos un elemento a la matriz m3.

            for i in range(len(self.m)): #Recorremos la matriz m1.
                for j in range(len(other.m[0])): #Recorremos la matriz m2.
                    for k in range(len(other.m)): #Recorremos la matriz m2.
                        m3[i][j] += self.m[i][k] * other.m[k][j] #Multiplicamos las matrices.
                
            #Retornando el resultado como matriz.
            return Matriz(m3)
        else: #Si las matrices no se pueden multiplicar, etnonces devolvemos un mensaje de error.
            return "Las matrices no se pueden multiplicar"
    
    def __add__(self, other): #Método para sumar dos matrices iguales.
        
        if len(self.m) == len(other.m) and len(self.m[0]) == len(other.m[0]): #Si las matrices tienen las mismas filas y columnas.
            m3 = [] #Creamos una matriz vacía para el resultado.

            for i in range(len(self.m)): #Se crea una matriz con las mismas dimensiones que m1 y m2.
                m3.append([])
                for j in range(len(self.m[0])):
                    m3[i].append(0)
            
            #Se recorre la matriz m3 y se le asigna el resultado de la suma de las matrices m1 y m2.
            for i in range(len(m3)):
                for j in range(len(m3[0])): 
                    m3[i][j] = self.m[i][j] + other.m[i][j] #Se suman los elementos de las matrices.
            
            return Matriz(m3) #Devolvemos el resultado.
        else: #Si las matrices no tienen las mismas dimensiones, entonces devolvemos un mensaje de error.
            return "Las matrices no tienen las mismas dimensiones"
    
    #Método para obtener el valor de un elemento de la matriz.
    def __getitem__(self, i):
        return self.m[i]
    
    #Método para imprimir la matriz.
    def __str__(self):
        return str(self.m)
