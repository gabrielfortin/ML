import json
from shapely.geometry import Polygon
from math import pi

import pandas as pd    
from sklearn.model_selection import train_test_split    
from sklearn.metrics import classification_report    
from sklearn.neighbors import KNeighborsClassifier 

from data.FeatureCollection import feature_collection_from_dict, GeometryType

# Measure compactness of the polygon with the Polsby-Popper method
def compute_compactness(geom: Polygon):
    p:float = geom.length
    a:float = geom.area    
    return (4*pi*a)/(p**2)


def load_data():
    rows = []
    with open('data/data.json') as json_file:
        collection = feature_collection_from_dict( json.load(json_file))
        
        for  feature in collection.features:
            if(feature.geometry.type == GeometryType.MULTI_POLYGON
                or  feature.properties.type == None):
                continue
            points = feature.geometry.coordinates[0]
            label = feature.properties.type.value
            area = feature.properties.superficie
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
