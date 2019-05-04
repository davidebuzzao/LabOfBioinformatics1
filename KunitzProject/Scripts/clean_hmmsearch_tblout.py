#!/usr/local/bin/python3
import sys

def hmmsearch_tblout(file_in, file_out, CLASS_SCORE = 0):
    with open(file_in) as FILE_IN, open(file_out, 'w') as FILE_OUT:    
        
        if "positive" in file_in:
            CLASS_SCORE = 1
        
        for line in FILE_IN:    
            if line.startswith('#'): continue
        
            SEQ_ID = line.split("|")[1]
            E_VAL = str(line.split()[4])
            E_DOM = str(line.split()[7])
            FILE_OUT.write(SEQ_ID + ' ' + E_VAL + ' ' + E_DOM + ' ' + str(CLASS_SCORE) + '\n')
    return()


if __name__ == '__main__':
    try:
        FILE_IN = sys.argv[1]
        FILE_OUT = sys.argv[2]
    except:
        print('Program Usage: text.py <HMMSEARCH_FILE> <FILE_OUT>')
        raise SystemExit
    else:
        hmmsearch_tblout(FILE_IN, FILE_OUT)