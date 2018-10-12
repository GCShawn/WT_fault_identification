from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree

def model_train (type, X_train, y_train, X_test, y_test):

    labels = ['no-fault','fault', 'other']
    
    if type == 'SVM':
        Cs = [0.1, 1, 10, 100, 1000]
        gammas = [1e-3, 1e-4, 1e-5]
        ##class_weight':[{0: w} for w in [1, 2, 10, 50, 100]]
        param_grid = {'C': Cs,
                      'gamma': gammas,
                      #'class_weight': [None],
                      'kernel': ['linear']}
        ##Class weight will increase the minority class by 1, 2, 10, 50 times
        
        clf = GridSearchCV(SVC(), param_grid, iid=True, cv = 10, verbose = 10)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        clfreport = classification_report(y_test, y_pred, target_names=labels)
        cm = confusion_matrix(y_test, y_pred)
        best_param = clf.best_params_
        
    if type == 'Decision Tree':
        model= DecisionTreeClassifier(random_state=1234)
        params = {'max_features': ['auto', 'sqrt', 'log2'],
                  'max_depth':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
                  'min_samples_split': [2,3,4,5,6,7,8,9,10,11,12,13,14,15], 
                  'min_samples_leaf':[1,2,3,4,5,6,7,8,9,10,11],
                  'random_state':[123]}
        clf = GridSearchCV(model, param_grid=params, n_jobs = 1)
        clf.fit(X_train, y_train)
        best_param = clf.best_params_
        #clf = DecisionTreeClassifier (criterion = 'gini', random_state = 100, max_depth = None)
        #clf.fit(X_train_bal, y_train_bal)
        y_pred = clf.predict(X_test)
        clfreport = classification_report(y_test, y_pred, target_names=labels)
        cm = confusion_matrix(y_test, y_pred)
        
    return clfreport, best_param, cm