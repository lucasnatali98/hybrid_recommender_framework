'''
Execute the scikit-learn tuning.

Created on 14/03/2016
Updated on 17/07/2017
@author: reifortes

Command line:
- python2.7

References:
- http://scikit-learn.org/stable/index.html
- http://scikit-learn.org/stable/modules/grid_search.html
- http://scikit-learn.org/stable/auto_examples/model_selection/randomized_search.html#example-model-selection-randomized-search-py
'''

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import sys
    import time
    from datetime import datetime
    import numpy as np
    from scipy.stats import uniform as uniform
    from scipy.stats import randint as randint
    from sklearn.datasets import load_svmlight_file
    from sklearn.linear_model import Ridge
    from sklearn.linear_model import BayesianRidge
    from sklearn.linear_model import SGDRegressor
    from sklearn.isotonic import IsotonicRegression
    from sklearn.ensemble import BaggingRegressor
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.ensemble import AdaBoostRegressor
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.svm import LinearSVR
    from sklearn.svm import SVR
    from sklearn.model_selection import GridSearchCV
    from sklearn.model_selection import RandomizedSearchCV
    from operator import itemgetter


# the strategy 'R' or 'G' noe is defined as a running parameter
algorithms = {
                'Ridge'    : ( Ridge(), {'alpha': uniform(0.1, 5.0), 'fit_intercept': [True, False]}, 'R' ),
                'B-Ridge'  : ( BayesianRidge(), {'n_iter': randint(100, 600), 'alpha_1': uniform(0.000001, 1), 'alpha_2': uniform(0.000001, 1), 'lambda_1': uniform(0.000001, 1), 'lambda_2': uniform(0.000001, 1)}, 'R' ),
                #'Bag'      : ( BaggingRegressor(n_jobs=-1, random_state=0), {'n_estimators': randint(10, 500), 'max_samples': randint(1, 50), 'max_features': randint(1, 50), 'bootstrap': [True, False], 'bootstrap_features': [True, False], 'oob_score': [True, False]}, 'R' ),
                'Bag'      : ( BaggingRegressor(n_jobs=1, random_state=0, bootstrap=True), {'n_estimators': randint(10, 500), 'max_samples': randint(1, 50), 'bootstrap_features': [True, False], 'oob_score': [True, False]}, 'R' ),
                #'RFR'      : ( RandomForestRegressor(n_jobs=-1, random_state=0), {'n_estimators': randint(10, 500), 'max_features': [None, randint(1, 50)], 'max_depth': [None, randint(1, 50)], 'min_samples_split': randint(2, 50), 'min_samples_leaf': randint(1, 50), 'min_weight_fraction_leaf': uniform(0.0, 1.0), 'max_leaf_nodes': [None, randint(1, 50)], 'bootstrap': [True, False], 'oob_score': [True, False]}, 'R' ),
                'RFR'      : ( RandomForestRegressor(n_jobs=-1, random_state=0, bootstrap=True), {'n_estimators': randint(10, 500), 'max_depth': randint(1, 50), 'min_samples_split': randint(2, 50), 'min_samples_leaf': randint(1, 50), 'min_weight_fraction_leaf': uniform(0.0, 0.5), 'max_leaf_nodes': randint(2, 50)}, 'R' ),
                'AdaB'     : ( AdaBoostRegressor(random_state=0), {'n_estimators': randint(10, 500), 'learning_rate': uniform(0.05, 2.0), 'loss': ['linear', 'square', 'exponential'] }, 'R' ),
                'GBR'      : ( GradientBoostingRegressor(random_state=0), {'n_estimators': randint(10, 500), 'learning_rate': uniform(0.05, 2.0), 'max_depth': randint(1, 50), 'min_samples_split': randint(2, 50), 'min_samples_leaf': randint(1, 50), 'min_weight_fraction_leaf': uniform(0.0, 0.5), 'max_leaf_nodes': randint(2, 50), 'subsample': uniform(0.0, 0.9), 'alpha': uniform(0.0, 1.0)}, 'R' ),
                'LinearSVR': ( LinearSVR(random_state=0), {'C': uniform(0.1, 1.5), 'loss': ['epsilon_insensitive', 'squared_epsilon_insensitive'], 'epsilon': uniform(0.0, 1.0), 'tol': uniform(0.00005, 0.005), 'fit_intercept': [True, False]}, 'R' ),
                #'SVR'      : ( SVR(max_iter=1000), {'C': uniform(0.1, 1.5), 'epsilon': uniform(0, 1.0), 'kernel': ['poly', 'rbf', 'sigmoid'], 'degree': randint(2, 5), 'coef0': uniform(0.0, 0.1), 'shrinking': [True, False], 'tol': uniform(0.0005, 0.005)}, 'R' ),
                'SVR'      : ( SVR(), {'C': uniform(0.1, 1.5), 'epsilon': uniform(0, 1.0), 'kernel': ['poly', 'rbf', 'sigmoid'], 'degree': randint(2, 5), 'coef0': uniform(0.0, 0.1), 'shrinking': [True, False], 'tol': uniform(0.0005, 0.005)}, 'R' ),
             }


# Utility function to report best scores
def report(search):
    print(f"\t\t- Best score: {search.best_score_:.6f}")
    print(f"\t\t- Parameters: {search.best_params_}\n")


if __name__ == '__main__':
    st = time.time()
    print("\nStarted")
    print(datetime.now())
    print("==============\n")
    print(sys.argv)

    dataset         = sys.argv[1]#ML1M
    scikitHome      = sys.argv[2]#Scikit/Tuning
    scikitFiles     = sys.argv[3].split(';')#['FWLS-01'; 'HR-01']
    algs            = sys.argv[4].split(';')#['Ridge'; 'B-Ridge']
    strategy        = sys.argv[5]#'R' = randomized; 'G' = Grid
    if len(sys.argv) > 6: cv = int(sys.argv[6])
    else: cv = 5
    if len(sys.argv) > 7: n_iter_search = int(sys.argv[6])
    else: n_iter_search = 100

    for alg in algorithms.keys():
        if alg not in algs: continue
        print("--------------\n")
        print('- Algorithm: ' + alg)
        for file in scikitFiles:
            print("..............\n")
            print('- File: ' + file)
            start = time.time()
            TrainFeatures, TrainOuts = load_svmlight_file('%s/%s/%s' % (dataset, scikitHome, file))
            #TrainFeatures = TrainFeatures.fillna(0) # Problem with NaN, using ZERO
            print("\t\t- Training took\t%.2f\tseconds." % ((time.time() - start)))
            start = time.time()
            if strategy == 'G': search = GridSearchCV(algorithms[alg][0], param_grid=algorithms[alg][1])
            else: search = RandomizedSearchCV(algorithms[alg][0], param_distributions=algorithms[alg][1], cv=cv, n_iter=n_iter_search, n_jobs=-1)
            search.fit(TrainFeatures.toarray(), TrainOuts)
            print("\t\t- RandomizedSearchCV took\t%.2f\tseconds\tfor %d candidates parameter settings." % ((time.time() - start), n_iter_search))
            report(search)

    et = time.time()
    ds = et - st
    dm = ds / 60
    print("==============\n")
    print("Finished in %2.2f sec / %2.2f min (EXE time)." % (ds, dm))
    print(datetime.now())
