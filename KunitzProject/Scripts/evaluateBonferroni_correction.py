#!/usr/local/bin/python3

import sys
    
def bonferroni_correction(file_in, set_dim, file_out):
    with open(file_in) as FILE_IN, open(file_out, 'w') as FILE_OUT:
        for line in FILE_IN:
            line = line.split()
            SEQ_ID, CLASS_SCORE = line[0], line[3]
            E_VAL = str(float(line[1]) / set_dim)
            E_DOM = str(float(line[2]) / set_dim)
            FILE_OUT.write(SEQ_ID + ' ' + E_VAL + ' ' + E_DOM + ' ' + CLASS_SCORE + '\n')
        return

if __name__ == '__main__':
    try:
        FILE_IN = sys.argv[1]
        SET_DIM = sys.argv[2]
        FILE_OUT = sys.argv[3]
    except:
        print('Program Usage: text.py <CLEAN_HMMSEARCH> <SET_DIMENSION> <FILE_OUT>')
        raise SystemExit
    else:
        bonferroni_correction(FILE_IN, float(SET_DIM), FILE_OUT)