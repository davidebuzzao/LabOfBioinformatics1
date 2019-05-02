#!/usr/local/bin/python3

import sys
import os

def get_ATOMlines(raw_pdb, chain, clean_pdb):
    with open(clean_pdb, 'w') as FILEOUT:
        for line in raw_pdb:
            if line[:4] != 'ATOM': continue
            if line[21] != chain: continue
            FILEOUT.write(line)
    return()


if __name__ == "__main__":
    try:
        LIST_PDB = sys.argv[1]
        PWD = sys.argv[2]
    except:
        print('Program usage: text.py <RAW_PDB> <WORKING_DIRECTORY>')
        raise SystemExit
    else:
        LIST_PDB = open(LIST_PDB)
        ID = []
        CHAIN = []
        for line in LIST_PDB:
            line.strip().split(':')
            ID.append(line.strip().split(':')[0].upper())
            CHAIN.append(line.strip().split(':')[1])
        
        dict_ID = dict([(i,j) for i, j in zip(ID, CHAIN)])
        for filename in os.listdir(PWD):
            if filename.endswith('.pdb'):
                with open(os.path.join(PWD, filename)) as f:
                    if filename.split('.')[0] in dict_ID:
                        get_ATOMlines(f, dict_ID[filename.split('.')[0]], filename.split('.')[0]+".cleanpdb")