# python -m scripts.gcforest

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score

from core.pdeas.model_manager import Model
from core.utils.constants import DATASET_IDS
from core.utils.data_util import load_data_by_id
from core.utils.env_util import environment_init, split_validation_data, get_gcf_cs_args
from core.utils.log_util import create_logger

# create logger to record result
logger = create_logger()

# must add, environment init
environment_init()

# load parsed arguments
args = get_gcf_cs_args()
id_, n_splits = args.data, args.n_splits

# set model
model = [0, 'RandomForestClassifier', 0, 'RandomForestClassifier', 0, 'RandomForestClassifier', 0,
         'RandomForestClassifier', 0, 'ExtraTreesClassifier', 0, 'ExtraTreesClassifier', 0,
         'ExtraTreesClassifier',
         0, 'ExtraTreesClassifier']

df = pd.DataFrame(index=DATASET_IDS)
id_to_score = {}
for id_ in DATASET_IDS:
    logger.info(f"Running on dataset {id_}...")
    # track scores
    scores = []
    for kth in range(n_splits):
        x_train, x_test, y_train, y_test = load_data_by_id(id_, kth)
        X_train, X_val, Y_train, Y_val = split_validation_data(x_train, y_train)
        model = [0, 'RandomForestClassifier', 0, 'RandomForestClassifier', 0, 'RandomForestClassifier', 0,
                 'RandomForestClassifier', 0, 'ExtraTreesClassifier', 0, 'ExtraTreesClassifier', 0,
                 'ExtraTreesClassifier',
                 0, 'ExtraTreesClassifier']
        gcforest = Model(model)
        gcforest.fit(X_train, Y_train, X_val, Y_val, confidence_screen=True)
        gcforest.refit(x_train, y_train)
        y_pred = gcforest.predict(x_test)
        acc = accuracy_score(y_test, y_pred)
        scores.append(acc)
        logger.info(f"{kth + 1}-th fold score: {acc}.")
    cvs = np.mean(scores)
    logger.info(f"Gcforest_cs on {id_}, {n_splits}-fold cross val score: {cvs}.\n")
    id_to_score[id_] = cvs
df['gcf_cs'] = pd.Series(id_to_score)
df.to_csv('gcforest_cs.csv')
