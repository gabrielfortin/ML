import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

dataFrame = pd.read_csv('IRIS.csv')
dataFrame.plot()
model = svm.SVC()

x = dataFrame.iloc[:,:4]
y = dataFrame.iloc[:,4]

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3)

model.fit(x_train, y_train)

prediction = model.predict(x_test)

print(classification_report(y_test, prediction))
