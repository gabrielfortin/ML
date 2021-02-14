import json
from shapely.geometry import Polygon
from math import pi, sqrt

import pandas as pd    
from sklearn import svm    
from sklearn.model_selection import train_test_split    
from sklearn.metrics import classification_report    
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from sklearn import neighbors


# Measure compactness of the polygon with the Polsby-Popper method
def compute_compactness(geom):
    p = geom.length
    a = geom.area    
    return (4*pi*a)/(p**2)


def load_data():
    rows = []
    with open('data.json') as json_file:
        data = json.load(json_file)
        for i, feature in enumerate(data['features']):
            if(feature["geometry"]["type"]=="MultiPolygon"):
                continue
            points = feature["geometry"]["coordinates"][0]
            label = feature["properties"]["TYPE"]
            area = feature["properties"]["SUPERFICIE"]
            compactness = compute_compactness(Polygon(points))
            rows.append([area,  compactness, label])
    df = pd.DataFrame(rows, columns=["area",  "compactness", "label"])
    df.dropna()
    return df.dropna()

    
def train(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3)    
    model = KNeighborsClassifier(n_neighbors=4)
    model.fit(x_train, y_train)    
    prediction = model.predict(x_test)    
    print(classification_report(y_test, prediction))
    return model

df = load_data()


X = df.iloc[:,:2]
y = df.iloc[:,2]
train(X,y)
