
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier

from core.utils.data_util import load_data_by_id
from core.utils.env_util import environment_init, get_MLP_args
from core.utils.log_util import create_logger

# create logger to record result
logger = create_logger()

# must add, environment init
environment_init()

# load parsed arguments
args = get_MLP_args()
id_, n_splits, hidden_layer_sizes = args.data, args.n_splits, args.hidden_layer_sizes

# track scores
scores = []

# n_splits cross validation
for kth in range(n_splits):
    x_train, x_test, y_train, y_test = load_data_by_id(id_, kth)
    clf = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes)
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    acc = accuracy_score(y_test, y_pred)
    scores.append(acc)
    logger.info(f"{kth + 1}-th fold score: {acc}.")
cvs = np.mean(scores)
logger.info(f"MLP on {id_}, {n_splits}-fold cross val score: {cvs}.")
