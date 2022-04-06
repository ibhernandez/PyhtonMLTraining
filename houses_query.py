# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 11:20:22 2022

@author: igbh
"""


import pandas as pd

# Open file
id = pd.read_csv("kc_house_data.csv")
# Clean file
id = id.fillna("UNKNOWN")
print(id.info())

#Pregunta 1: ¿Cuál es la casa de mayor precio?
exp = id.loc[id["price"].idxmax()]
print("id: " +str(exp["id"])+" price: "+str(exp["price"])+ " zipcode: "+str(exp["zipcode"]))


#Pregunta 2: ¿Cuál es la vivienda más pequeña (tamaño habitable)?
exp = id.loc[id["sqft_living"].idxmin()]
print("id: " +str(exp["id"])+" sqft_living: "+str(exp["sqft_living"])+ " zipcode: "+str(exp["zipcode"]))


#Pregunta 3: ¿La casa más pequeña (metros habitables) es también la más barata?
exp = id.loc[id["sqft_living"].idxmin()]
exp1 = id.loc[id["price"].idxmin()]
if exp["id"] == exp1["id"]:
    print("Yes, its the same")
else:
    print("No, its different")
    
print("Smallest house id: " +str(exp["id"])+" sqft_living: "+str(exp["sqft_living"])+ " price: "+str(exp["price"]))
print("Cheapest house id: " +str(exp1["id"])+" sqft_living: "+str(exp1["sqft_living"])+ " price: "+str(exp1["price"]))


#Pregunta 4: Mostrar una distribución de los precios de las viviendas
id[["price"]].hist(bins=1000)


#Pregunta 5: De entre las casas de mejor calidad del edificio, ¿cuál es la que tiene un mejor estado y que, además, sea lo más barato posible?
print("sorted by highest grade, best condition and as cheapest as possible")
d_sel = id[["id", "grade", "condition", "price", "sqft_living", "zipcode"]]
print(d_sel.sort_values(by=["grade", "condition", "price"], ascending=[False, False, True]).head())


#Pregunta 6: ¿Cuántas viviendas hay por cada categoría de calidad de edificio?
print("houses per grade")
print(id["grade"].value_counts())


#Pregunta 7: ¿Las vistas son generalmente mejores en casas que miran a la costa?
print("waterfront vs view")
d_sel = id[["id", "grade", "price", "waterfront", "view", "zipcode"]]
print(d_sel.sort_values(by=["grade", "waterfront", "view"], ascending=[False, False, False]).head())
print("As waterfront has a value of 0 in the top 5, we conclude that  waterfront has no influence in the view")


#Pregunta 8: ¿Cuáles son las áreas (en función del código postal) más caros y que precio medio tienen? ¿Cuáles los más baratos?

d_sel = id[["zipcode", "price"]].groupby(["zipcode"]).mean()
print("Most expensive by zipcode: ")
print(d_sel.sort_values(by=["price"], ascending=[False]).head())
print("Cheapest by zipcode:")
print(d_sel.sort_values(by=["price"], ascending=[True]).head())


#Pregunta 9: ¿Cuál es la casa más antigua y cuál es la más cara?
print("Oldest house")
print(id[["id", "zipcode", "date", "price"]].sort_values(by=["date"], ascending=[True]).head(1))
print("Most expesive house")
print(id[["id", "zipcode", "date", "price"]].sort_values(by=["price"], ascending=[False]).head(1))


#Pregunta 10: ¿Cuál es la casa más grande (tamaño útil) y con menos de 1 habitación?
print("Biggest house with less than one room")
d_filter = id[id["bedrooms"]<1]     
print(d_filter[["id", "zipcode", "sqft_living", "price", "bedrooms"]].sort_values(by=["sqft_living"], ascending=[False]).head(1))