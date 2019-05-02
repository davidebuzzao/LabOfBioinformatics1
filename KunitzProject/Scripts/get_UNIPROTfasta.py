#!/usr/local/bin/python3

import sys

def parsingFASTA_UNIPROT(dict_id, db, file_out):
    DICT_ID = dict_id
    with open(db, 'r') as DB: 
        with open(file_out, 'w') as FILE_OUT:
    
            header = ''
            sequence = ''
            
            for line in DB:
                if header and sequence:
                    if line[0] == '>':
                        FILE_OUT.write(header + sequence)
                        header = ''
                        sequence = ''
                
                if line[0] == '>':
                    ID = str(line.split("|")[1])
                    if DICT_ID.get(ID, False):
                        header = line
                        del DICT_ID[ID]

                else:
                    if header:
                        sequence += line
            
            if header and sequence:
                FILE_OUT.write(header + sequence)

if __name__ == '__main__':
    try:
        LIST_ID = sys.argv[1]
        DB = sys.argv[2]
        FILE_OUT = sys.argv[3]
    except:
        print('Program Usage: text.py <LIST_FILE> <DB_FILE> <FILE_OUT>')
        raise SystemExit
    else:
        DICT_ID = dict([(i,True) for i in open(LIST_ID).read().split('\n')])
        parsingFASTA_UNIPROT(DICT_ID, DB, FILE_OUT)