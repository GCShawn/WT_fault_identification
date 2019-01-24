from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.utils import class_weight
import numpy as np


def model_train (type, X_train, y_train, X_test, y_test):
    
    if type == 'SVM':
        Cs = [1, 10, 100]
        gammas = [1e-4, 1e-3, 1e-5]
        class_weights = class_weight.compute_class_weight('balanced', np.unique(y_train), y_train)
        param_grid = {'C': Cs,
                      'gamma': gammas,
                      'kernel': ['linear']}
        
        clf = GridSearchCV(SVC(), param_grid, class_weight = class_weights, scoring = 'recall_weighted', iid=True, cv = 10, verbose = 10)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        best_param = clf.best_params_
        
    if type == 'DT':
        model= DecisionTreeClassifier(random_state=1234)
        params = {'max_features': ['auto', 'sqrt', 'log2'],
                  'max_depth':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
                  'min_samples_split': [2,3,4,5,6,7,8,9,10,11,12,13,14,15], 
                  'min_samples_leaf':[1,2,3,4,5,6,7,8,9,10,11],
#                  'class_weight': [{0: 0.50941764, 30: 27.0459364}],
                  'random_state':[123]}
		class_weights = class_weight.compute_class_weight('balanced', np.unique(y_train), y_train)
        
		clf = GridSearchCV(model, param_grid=params, class_weight = class_weights, cv=10, n_jobs = 1)
        clf.fit(X_train, y_train)
        best_param = clf.best_params_
        y_pred = clf.predict(X_test)

        
    return y_pred, best_param