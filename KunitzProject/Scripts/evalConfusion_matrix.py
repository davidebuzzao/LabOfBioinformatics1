#!/usr/local/bin/python3

import sys
import matplotlib.pyplot as plt
import numpy as np    
from sklearn import metrics
import itertools
import seaborn as sns

def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        title = "Normalized confusion matrix"
        print(title)
    else:
        title = "Confusion matrix, without normalization"
        print(title)

    print(cm)
    
    ax = plt.subplot()
    sns.heatmap(cm, vmin=0, vmax=350, annot=True, fmt='', cbar=True) ## annot = True to annotate cells

    ## labels, title and ticks
    ax.set_xlabel('Predicted labels'); ax.set_ylabel('True labels') 
    ax.set_title(title); 
    ax.xaxis.set_ticklabels(['Non Kunitz', 'Kunitz'])
    ax.yaxis.set_ticklabels(['Kunitz', 'Non Kunitz'])
 

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        iteration = sys.argv[2]
        if iteration == 'NO':
            threshold = float(sys.argv[3])
    
        score_position = -2 
        class_position = -1
    except:
        if iteration == 'YES':
            print('Program Usage: script.py <PREDICTION_FILE.TXT> <ITERATION = YES/NO>')
            raise SystemExit
        if iteration == 'NO':
            print('Program Usage: script.py <PREDICTION_FILE.TXT> <ITERATION = NO> <THRESHOLD>')
            raise SystemExit
    else:
        if iteration == 'YES': 
            THR_LIST = [0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001, 0.00000001, 0.000000001, 0.0000000001]
            BEST_MCC = (-1.0, 0.0)
            for threshold in THR_LIST:
                with open(filename, 'rt') as FILE_IN:
                    Y_TRUE = []
                    Y_PRED = []

                    ### OPTIMIZATION PROCEDURE ###
                    for line in FILE_IN:
                        Y_TRUE.append(int(line.rstrip().split()[-1]))
                        
                        if float(line.rstrip().split()[-2]) >= threshold:
                            Y_PRED.append(int(0))
                        else: 
                            Y_PRED.append(int(1))
                    MCC = metrics.matthews_corrcoef(Y_TRUE, Y_PRED,  sample_weight=None)   
                    if MCC > BEST_MCC[0]:
                        BEST_MCC = (MCC, threshold)
                    ACC = metrics.accuracy_score(Y_TRUE, Y_PRED, normalize=True, sample_weight=None)
                    PPV = metrics.precision_score(Y_TRUE, Y_PRED, labels=None, pos_label=1, average='binary', sample_weight=None)
                    
                    ### Compute confusion matrix ###
                    CNF_MATRIX = metrics.confusion_matrix(Y_TRUE, Y_PRED)
                    FPR, TPR, THRESHOLDS = metrics.roc_curve(Y_TRUE, Y_PRED, pos_label=1)
                    TNR = 1.0 - FPR
                    np.set_printoptions(precision=2)
                    print('\nE-value threshold: ', threshold, '\n\nMCC:\t', MCC, '\nACC:\t', ACC, '\nPPV:\t', PPV, '\nTNR:\t', TNR, '\nTPR:\t', TPR, '\n')

            with open(filename, 'rt') as FILE_IN:
                    Y_TRUE = []
                    Y_PRED = []
                    
                    ### OPTIMIZATION PROCEDURE ###
                    for line in FILE_IN:
                        Y_TRUE.append(int(line.rstrip().split()[-1]))
                        
                        if float(line.rstrip().split()[-2]) >= BEST_MCC[1]:
                            Y_PRED.append(int(0))
                        else: 
                            Y_PRED.append(int(1))
                    CNF_MATRIX = metrics.confusion_matrix(Y_TRUE, Y_PRED)
                    np.set_printoptions(precision=2)
                    print('\nBest e-value threshold: ', BEST_MCC[1], '\n')

                    ### Plot confusion matrix ###
                    plt.figure()
                    PLOT = plot_confusion_matrix(CNF_MATRIX, classes=['NON_KUNITZ','KUNITZ'])
                   
        else:
            with open(filename, 'rt') as FILE_IN:
                    Y_TRUE = []
                    Y_PRED = []
                    
                    ### OPTIMIZATION PROCEDURE ###
                    for line in FILE_IN:
                        Y_TRUE.append(int(line.rstrip().split()[-1]))
                        
                        if float(line.rstrip().split()[-2]) >= threshold:
                            Y_PRED.append(int(0))
                        else: 
                            Y_PRED.append(int(1))
                    
            ### Compute confusion matrix ###
            CNF_MATRIX = metrics.confusion_matrix(Y_TRUE, Y_PRED)
            np.set_printoptions(precision=2)
            MCC = metrics.matthews_corrcoef(Y_TRUE, Y_PRED,  sample_weight=None)   
            ACC = metrics.accuracy_score(Y_TRUE, Y_PRED, normalize=True, sample_weight=None)
            PPV = metrics.precision_score(Y_TRUE, Y_PRED, labels=None, pos_label=1, average='binary', sample_weight=None)
            print('\nE-value threshold: ', threshold, '\n\nMCC:\t', MCC, '\nACC:\t', ACC, '\nPPV:\t', PPV, '\n')
        
            ### Plot confusion matrix ###
            plt.figure()
            PLOT = plot_confusion_matrix(CNF_MATRIX, classes=['NON_KUNITZ','KUNITZ'])
            
            if 'CVset' in filename:
                plt.savefig('CVset_ConfMat.pdf', box_inches='tight')
            else:
                plt.savefig('TESTset_ConfMat.pdf', box_inches='tight')