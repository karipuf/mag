from sys import stdout
import pandas as pd
import re
from itertools import count

paperFile="MechanicalEngineeringSelectedPapers.txt"
referencesFile="PaperReferences.txt"
outFile='MechanicalEngineeringSelectedPaperReferences.txt'

# Getting the Mechanical Engineering paper IDs
pids=set(pd.read_csv(paperFile,'\t',header=None,usecols=[0],names=['pid']).pid)

# Reading the PaperAuthorAffiliations file
with open(referencesFile,'r') as f:

    # Set up
    fi=iter(f)
    counter=count(1)
    pidreg=re.compile('\S+')

    # Filtering the file
    with open(outFile,'w+') as of:
        for l in fi:
            refpids=pidreg.findall(l)
        
            if (refpids[0] in pids) and (refpids[1] in pids):
                of.write("\t".join(refpids)+'\n')

            # Counting...
            c=next(counter)
            if c % 100000==0:
                print("Processed line #"+str(c))
                stdout.flush()
