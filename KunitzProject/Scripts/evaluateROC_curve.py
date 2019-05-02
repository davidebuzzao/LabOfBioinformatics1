#!/usr/local/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import average_precision_score, roc_curve, auc, precision_recall_curve, roc_auc_score
from sklearn.utils.fixes import signature
from seaborn import lineplot

def ROC_curve(filename, score_position, class_position):
    
    ## The roc curve function from sklearn.metrics is given in input two arrays: 
    ## one with predicted scores, the other one with class score. 
    y_pred = []
    y_true = []

    with open(filename) as FILE_IN:
        for line in FILE_IN:
            y_pred.append(-float(line.rstrip().split()[score_position])) ## put -float(number) since the ROC built_in() function will take the greater number 
            y_true.append(int(line.rstrip().split()[class_position]))    ## than a given threshold as positive values. 

        Y_PRED = np.array(y_pred)
        Y_TRUE = np.array(y_true)
        FPR, TPR, THRESHOLDS = roc_curve(Y_TRUE, Y_PRED, pos_label=1)
        
        ## Compute Area Under the Receving Operating Characteristic Curve from prediction scores
        ROC_AUC_SCORE = roc_auc_score(Y_TRUE, Y_PRED)
        print('ROC AUC score: {0:0.2f}'.format(ROC_AUC_SCORE))

        ## Plot the ROC curve and fill its AUC
        step_kwargs = ({'step': 'post'} 
                        if 'step' in signature(plt.fill_between).parameters 
                        else {})
        plt.step(FPR, TPR, color='r', alpha=1.0,
                where='post')
        plt.fill_between(FPR, TPR, alpha=0.5, color='r', **step_kwargs)

        ## Label the architecture of the graph 
        plt.ylabel('TPR')
        plt.xlabel('FPR')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title('Receiver Operating Characteristic curve : ROC={0:0.2f}'.format(ROC_AUC_SCORE))
        
        ## Show OR save the figure
        #plt.show()
        plt.savefig('ROC_curve.pdf', box_inches='tight')

def PR_curve(filename, score_position, class_position):
   
    ## The Precision-Recall curve function from sklearn.metrics is given in input two arrays: 
    ## one with predicted scores, the other one with class score. 
    y_pred = []
    y_true = []

    with open(filename) as FILE_IN:
        for line in FILE_IN:
            y_pred.append(-float(line.rstrip().split()[score_position]))
            y_true.append(int(line.rstrip().split()[class_position]))
        Y_PRED = np.array(y_pred)
        Y_TRUE = np.array(y_true)
        precision, recall, thresholds = precision_recall_curve(Y_TRUE, Y_PRED)
        
        average_precision = average_precision_score(Y_TRUE, Y_PRED)
        print('Average precision-recall score: {0:0.2f}'.format(average_precision))

        ## Plot the ROC curve and fill its AUC
        step_kwargs = ({'step': 'post'} 
                        if 'step' in signature(plt.fill_between).parameters 
                        else {})
        plt.step(recall, precision, color='g', alpha=1.0, where='post')
        plt.fill_between(recall, precision, alpha=0.5, color='g', **step_kwargs)

        ## Label the architecture of the graph
        plt.xlabel('TPR')
        plt.ylabel('PPV')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title('2-class Precision-Recall curve: AP={0:0.2f}'.format(average_precision))
        
        ## Show OR save the figure
        #plt.show()
        plt.savefig('PrecisionRecall_curve.pdf', box_inches='tight')

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        score_position = -2 
        class_position = -1
    except:
        print('Program Usage: script.py <PREDICTION_FILE.TXT>')
        raise SystemExit
    else:
        ROC_curve(filename, score_position, class_position)
        PR_curve(filename, score_position, class_position)