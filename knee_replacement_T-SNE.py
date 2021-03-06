import numpy as np
import pandas as pd
from sklearn.preprocessing import scale
from scipy._lib.six import xrange
import numpy as np

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
%matplotlib inline 


## Input file
X = pd.read_csv('Aqua_Knee.csv')

#Random split
msk = np.random.rand(len(X)) < 0.2
train = X[msk]
Hold_out = X[~msk] ### Will use later

## Convert Bool to 0/1 
X['is_aqua'] *= 1
X['trans'] *= 1
X['infection_knee'] *=1

## Dummy code out variables 
dummies = pd.get_dummies(X['Patient_Race_Code']).rename(columns=lambda x: 'Race_' + str(x))
X = pd.concat([X, dummies], axis=1)
X = X.drop(['Patient_Race_Code'], axis=1)

dummies = pd.get_dummies(X['Patient_Sex']).rename(columns=lambda x: 'Sex_' + str(x))
X = pd.concat([X, dummies], axis=1)
X = X.drop(['Patient_Sex'], axis=1)

dummies = pd.get_dummies(X['weekdays']).rename(columns=lambda x: 'W_' + str(x))
X = pd.concat([X, dummies], axis=1)
X = X.drop(['weekdays'], axis=1)

dummies = pd.get_dummies(X['ASA_MAPPED_SCOR_CD']).rename(columns=lambda x: 'ASA_' + str(x))
X = pd.concat([X, dummies], axis=1)


## Main Functions
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import manifold
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def run_tsne(train, target):
    sss = StratifiedShuffleSplit(target, test_size=0.2)
    for train_index, test_index in sss:
        break

    X_train, X_valid = train[train_index], train[test_index]
    Y_train, Y_valid = target[train_index], target[test_index]

    train_norm = normalize(X_valid, axis=0)
    tsne = manifold.TSNE(n_components=3,
                         init='pca',
                         perplexity=15,
                         random_state=101,
                         method='barnes_hut',
                         n_iter=2000,
                         verbose=2)
    train_tsne = tsne.fit_transform(train_norm)
    return (train_tsne, Y_valid)


def tsne_vis(tsne_data, tsne_groups):
    colors = cm.rainbow(np.linspace(0, 1, 5))
    labels = ['ASA_1', 'ASA_2' ,'ASA_3', 'ASA_4']

    plt.figure(figsize=(10, 10))
    for l, c, co, in zip(labels, colors, range(4)):
        plt.scatter(tsne_data[np.where(tsne_groups == co), 0],
                    tsne_data[np.where(tsne_groups == co), 1],
                    marker='o',
                    color=c,
                    linewidth='1',
                    alpha=0.8,
                    label=l)
    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 2')
    plt.title('t-SNE on 10% of train samples')
    plt.legend(loc='best')
    plt.savefig('rainbow-01.png')
    plt.show(block=False)

    plt.figure(figsize=(10, 10))
    for l, c, co, in zip(labels, colors, range(5)):
        plt.scatter(tsne_data[np.where(tsne_groups == co), 0],
                    tsne_data[np.where(tsne_groups == co), 2],
                    marker='o',
                    color=c,
                    linewidth='1',
                    alpha=0.8,
                    label=l)
    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 3')
    plt.title('t-SNE on 10% of train samples')
    plt.legend(loc='best')
    plt.savefig('rainbow-02.png')
    plt.show(block=False)

    plt.figure(figsize=(10, 10))
    for l, c, co, in zip(labels, colors, range(5)):
        plt.scatter(tsne_data[np.where(tsne_groups == co), 1],
                    tsne_data[np.where(tsne_groups == co), 2],
                    marker='o',
                    color=c,
                    linewidth='1',
                    alpha=0.8,
                    label=l)
    plt.xlabel('Dimension 2')
    plt.ylabel('Dimension 3')
    plt.title('t-SNE on 10% of train samples')
    plt.legend(loc='best')
    plt.savefig('rainbow-03.png')
    plt.show(block=False)


def map_column(table, f):
    labels = sorted(table[f].unique())
    mappings = dict()
    for i in range(len(labels)):
        mappings[labels[i]] = i
    table = table.replace({f: mappings})
    return table
    
    
## Plug in what you need here ##

X = train_df.drop(['Sex_F'], axis=1).values 
Y = train_df[['ASA_MAPPED_SCOR_CD']].values

tsne_data, tsne_groups = run_tsne(X, Y)
tsne_vis(tsne_data, tsne_groups)
