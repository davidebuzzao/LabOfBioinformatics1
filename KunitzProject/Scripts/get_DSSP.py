#!/usr/local/bin/python3

import sys

Norm_Acc={
            "A" :106.0,  "B" :160.0, \
            "C" :135.0,  "D" :163.0,  "E" :194.0, \
            "F" :197.0,  "G" : 84.0,  "H" :184.0, \
            "I" :169.0,  "K" :205.0,  "L" :164.0, \
            "M" :188.0,  "N" :157.0,  "P" :136.0, \
            "Q" :198.0,  "R" :248.0,  "S" :130.0, \
            "T" :142.0,  "V" :142.0,  "W" :227.0, \
            "X" :180.0,  "Y" :222.0,  "Z" :196.0
            }

def pretty_matrix(M):
    for element in M:
        print('\t'.join([str(i) for i in element]))


def parse_dssp(dssp_file, ch, surface):   
    
    with open(dssp_file, 'r') as FILE_IN:
        dssp = []
        dssp2 = []
        c = 0

        for line in FILE_IN:
            if line.find('  #  RESIDUE') == 0: ## when --# Residue appears in line
                c = 1
                continue
            if c == 0: continue 
            if line[13] == '!': continue
            if line[11] == ch or ch == '_':
                r = line[13].upper()
                c = line[11].upper()
                pos = line[5:10].strip()
                ss = line[16]
                if ss == ' ': ss = 'C' ## for coils there's empty space
                acc = float(line[35:38])
                phi = float(line[103:109])
                psi = float(line[109:115])
                racc = round(min(acc/Norm_Acc[r], 1.0), 4) #relative accessibility
                v = [r, pos, c, ss, acc, racc, phi, psi]
                v2 = [r, pos, c, acc]
                dssp2.append(v2)
                dssp.append(v)
        
        if surface == 'NO':
            return(dssp)

        if surface == 'YES':
            return(dssp2)
            

def find_surface(dssp_monomer, dssp_complex, chain, surface):
    DSSP_MONOMER = parse_dssp(dssp_monomer, chain, surface)
    DSSP_COMPLEX = parse_dssp(dssp_complex, chain, surface)
    INTERACT = []
    for i, j in zip(DSSP_MONOMER, DSSP_COMPLEX):
        if float(i[3]) == float(j[3]): continue
        else: 
            i.append(float(i[3]) - float(j[3]))
            INTERACT.append(i)
    
    return(INTERACT)

if __name__ == '__main__':
    
    try:
        DSSP_MONOMER = sys.argv[1]
        CHAIN = sys.argv[2]
        FIND_SURFACE = sys.argv[3]
    except:
        if FIND_SURFACE == 'YES':
            print('Program Usage: text.py <DSSP_MONOMER> <CHAIN> <YES> <DSSP_COMPLEX>')
            raise SystemExit
        elif FIND_SURFACE == 'NO':
            print('Program Usage: text.py <DSSP_MONOMER> <CHAIN> <NO>')
            raise SystemExit
    else:
        if FIND_SURFACE == 'YES':
            DSSP_COMPLEX = sys.argv[4]
            INTERACT = find_surface(DSSP_MONOMER, DSSP_COMPLEX, CHAIN, FIND_SURFACE)
            pretty_matrix(INTERACT)
        else:
            DSSP = parse_dssp(DSSP_MONOMER, CHAIN, FIND_SURFACE)
            pretty_matrix(DSSP)