#!/usr/local/bin/python3

import sys

def get_dict(filename):
    d = {}
    for line in filename:
        v = line.rstrip().split()
        d[v[0]] = float(v[-1])
    return(d)

def sort_cluster(clist, d):
    tlist = []
    for pid in clist:
        v = d.get(pid, float('inf'))
        tlist.append([v, pid])
    tlist.sort()
    return(tlist)

if __name__ == '__main__':
    try:
        FILE_IN1 = open(sys.argv[1], 'r')
        FILE_IN2 = open(sys.argv[2], 'r')
        FILE_OUT = open(sys.argv[3], 'w')
    except:
        print('Program Usage: text.py <PDB_ID+RESOLUTION> <BLASTCLUST_FILE> <OUTPUT_FILE>')
        raise SystemExit
    else:
        d = get_dict(FILE_IN1)
        
        for line in FILE_IN2:
            lid = line.rstrip().split()
            slid = sort_cluster(lid, d)
            print(len(slid), ' '.join([i[1] + ":" + str(i[0]) for i in slid]))