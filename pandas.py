# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 09:00:47 2022

@author: igbh
"""

import pandas as pd
from sqlite3 import connect
from IPython.display import display

#Introduccion
data_in = pd.read_csv("train.csv")      #, dtype={'Fare':'str'})  # Se abre el fichero y se puede indicar que alguna coñumna pase a string
#data_in = pd.read_excel("train.xlsx")  #, sheet_name = "name") #En vez de leer un csv, leemos un excel
print(data_in.head(10))                 # Muestra los 10 primeros resultados
display(data_in)                        # Muestra toda la tabla
print(data_in.dtypes)                   # Indica los tipos de las distintas columnas
print(data_in.info())                   # Muestra informacion de las columnas



#Seleccion basica de datos
d_sel = data_in[["PassengerId", "Fare"]]    # seleccionar columnas concretas de la tabla
d_sel = data_in[:7]                         # Selecciona las 7 primeras filas
d_sel = data_in [250:260][["PassengerId", "Survived"]]  # Selecciona las filas compredidas entre los dos extremos, sin incluir el ultimo y muestra solo los id de los pasajeros
display(d_sel)
#Edicion básica de tipos de datos
col_to_modify = ["Age", "PassengerId", "Survived"]          # Columnas a convertir
#data_in[col_to_modify] = data_in[col_to_modify].astype(str) # Cambia el tipo de una columna y lo sobrescribe
#data_in = data_in.astype(str)                              # Cambia todo a string y lo sobrescribe
print(data_in.dtypes)
display(data_in)

#Series y dataFrames
index ="PassengerId"
value = "Survived"
series = pd.Series(data = data_in[value], index = data_in[index])   #Obtenemos una serie de datos 
display(series)


#Crear un objeto dataframe
df_data = {                                             # Creeamos un nuevo objeto 
     "column_1": [1, 2, 3, 4, 5],
     'column_2': ['ES', 'ES', 'UK', 'FR', 'PT']
     }
df_new = pd.DataFrame(df_data)                          # Creamos una nueva tabla en base al objeto anterior

print(df_new.head())
df_new.to_csv ("test_IBH.csv", index=False)             # Se guarda la tabla en un csv

#Bases de datos relacionales
conn = connect(':memory:')                                                  # Crea una base de datos temporal en memoria
df = pd.DataFrame( data=[[0, "10/11/12"], [1, "11/12/13"]],                 # Crea una tabla con datos 
                   columns = ['int_column', 'date_column']
                  )
df.to_sql('test_data', conn)                                                # Añade la tabla a la BBDD
s_read = pd.read_sql('SELECT int_column, date_column FROM test_data', conn) #Obtiene los datos de la tabla
print(s_read)


#Funciones avanzadas de pandas sobre data_in
data_in[['dummy_col']] = 0                                                  # Crea una nueva columna rellena de 1
#data_in[['dummy_col']] = data_in[["PassengerId"]]+1                        # Suma 1 al id del pasajero y lo almacena en la dummy_col
data_in["dummy_col"] = data_in.apply(
    lambda x: (x["dummy_col"] + x["PassengerId"])*x["Survived"], axis =1)   # Operaciones que implican varias columnas
'''
data_in["dummy_col"] = data_in.apply(                                       # Operaciones que implican condiciones
    lambda x: x["dummy_col"] if x["Survived"] == 1
               else x["dummy_col"], axis =1)                                
'''

print(data_in.head())

#Filtrado de datos
d_filter = data_in[data_in["Survived"]==1]              #Tabla donde d_filter contiene solo a los supervivientes

d_filter = data_in[                                     #Se aplican varios filtros, supervivientes embarcados en tipo S y con tasa mayor que 70
    (data_in["Survived"] == 1) &
    ((data_in["Embarked"] == "S")|(data_in["Embarked"] == "C") )& # o usar isin(['S', 'C'])
    (data_in["Fare"] >= 70)
    ]
print(d_filter.head())

#Obtenion de distribuciones
dist = data_in["Embarked"].value_counts()           #Obtener el conteo del tipo de embarcados
print(dist)
dist = data_in["Sex"].value_counts()
print(dist)
dist = data_in["Survived"].value_counts()
print(dist)
#data_in["Age"].hist()                               # Mostrar el histograma de la distribucion de edades

#Limpieza de datos
'''
print("Shape before clean "+ str(data_in.shape))
data_in = data_in.dropna(subset = ["Embarked"])     #Limpiar los valores vacios de la columna embarked
print("Shape after clean "+ str(data_in.shape))
data_in = data_in["Cabin"].fillna("UNKNOWN")        # Rellenar los valores vacios de la columna Cabin

print(data_in)
'''

#Ejercicios:

# 1) Cuantas personas murieron en el hundimiento
aux_table = data_in[data_in["Survived"]==0]     # Filtro de personas que murieron survived =0 Esto no hace falta hacerlo
dist= aux_table["Survived"].value_counts()      # Conteo
print("Survivors: "+str(dist[0]))               # dist =[0 342] 342 valores con 0 en la columna Survived y por tanto nº personas que murieron dist[key]


# 2) Cuál fue el puerto donde embarcó más gente
dist = data_in["Embarked"].value_counts()
if dist["S"] >= dist["C"] and dist["S"] >= dist["Q"]:
    print("Place: S "+str(dist["S"]))
if dist["C"] >= dist["S"] and dist["C"] >= dist["Q"]:
    print("Place: C "+str(dist["C"]))
if dist["Q"] >= dist["C"] and dist["Q"] >= dist["S"]:
    print("Place: Q "+str(dist["Q"]))


# 3) Cuál fue el puerto donde subieron más pasajeros que luego sobrevivieron
at = data_in[data_in["Survived"]==1]
dist = at["Embarked"].value_counts()
if dist["S"] >= dist["C"] and dist["S"] >= dist["Q"]:
    print("Place: S "+str(dist["S"]))
if dist["C"] >= dist["S"] and dist["C"] >= dist["Q"]:
    print("Place: C "+str(dist["C"]))
if dist["Q"] >= dist["C"] and dist["Q"] >= dist["S"]:
    print("Place: Q "+str(dist["Q"]))
    
    
# 4) Cuál es la edad más habitual entre las personas que murieron
aux_table = data_in[data_in["Survived"]==0]     # Filtro de personas que murieron survived =0 Esto no hace falta hacerlo
aux_table["Age"].hist()


# 5) Se salvó el mismo porcentaje de hombres que de mujeres
aux_table = data_in[data_in["Survived"]==1]
dist= aux_table["Sex"].value_counts()
total= dist["male"]+dist["female"]
if ( dist["male"] == dist["female"]):
    print("Equal sex distribution, 50%")
else:
    print("Different distribution of deaths within sex-> Male: "+str(dist["male"])+", "+str(dist["male"]/total) +". Female: "+str(dist["female"])+", "+str(dist["female"]/total))
    
    
# 6) Cuál es el precio medio por ticket por clase de pasajero
p1 = data_in[data_in["Pclass"] == 1]
print("1: "+str(p1["Fare"].mean()))
p2 = data_in[data_in["Pclass"] == 1]
print("2: "+str(p2["Fare"].mean()))
p3 = data_in[data_in["Pclass"] == 1]
print("3: "+str(p3["Fare"].mean()))

# 7) Influyó la clase del pasajero en que se salvase o no
aux_table = data_in[data_in["Survived"]==0]     # Filtro de personas que murieron survived =0 Esto no hace falta hacerlo
dist= aux_table["Pclass"].value_counts()      # Conteo
total = len(aux_table)
if ( dist[3] == dist[2] == dist[1]):
    print("Equal class distribution, 50%")
else:
    print("Different distribution of deaths within class-> 1: "+str(dist[1])+", "+str(dist[1]/total) +". 2: "+str(dist[2])+", "+str(dist[2]/total)+". 3: "+str(dist[3])+", "+str(dist[3]/total))


# 8) Qué pasajeros de primera clase pagaron más por sus tickets, cuáles pagaron menos
print(data_in.sort_values(by=["Pclass", "Fare"], ascending=[True, False]).head())
print(data_in.sort_values(by=["Pclass", "Fare"], ascending=[False, True]).head())
