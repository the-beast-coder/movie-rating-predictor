import os
import numpy as np
import pandas as pd
from sklearn import tree
import math

def stringToInt(string):
    integer = 0
    #try seeing if string value given is already a number if so the output would be
    try:
        #means string value given is already a int
        integer = int(string)
    except:
        string = string.lower()
        for i in string:
            integer += ord(i)
    return integer

data = pd.read_csv("movies2.csv",encoding="latin-1")

data = data.values.tolist()

X_train = []
y_train = []


for i in range(len(data)):
    X_train.append([data[i][2], data[i][3], data[i][4], data[i][5], data[i][6]])
    y_train.append(data[i][1])

for i in range(len(X_train)):
    for x in range(len(X_train[i])):
        X_train[i][x] = stringToInt(X_train[i][x])

for i in range(len(y_train)):
    y_train[i] = int(float(y_train[i])*10)


model = tree.DecisionTreeClassifier()


model.fit(X_train, y_train)

director = input("Enter the name of the director: ")
director = director.lower()
director = stringToInt(director)

actor1 = input("Enter the name of the first actor: ")
actor1 = actor1.lower()
actor1 = stringToInt(actor1)

actor2 = input("Enter the name of the second actor: ")
actor2 = actor2.lower()
actor2 = stringToInt(actor2)

genre = input("Enter the main genre of the movie: ")
genre = genre.lower()
genre = stringToInt(genre)

budget = int(input("Enter the budget for the movie: "))

prediction = model.predict([[genre, actor1, director, actor2, budget]])

print(prediction[0]/10)
