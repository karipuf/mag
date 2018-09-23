import pandas as pd
import pickle,re
from ethnicity_funcs import name2ethnicity
from itertools import chain
from copy import deepcopy
from numpy.random import choice

#####################
# Utility functions
#####################


def Gini(collection):
    freq=pd.value_counts(collection)
    return 1-((freq/freq.sum())**2).sum()

def Collabs(aid,aid2pids,pid2aids):
    '''
    Returns collaborators for an author
    '''
    pids=aid2pids[aid]
    aids=[pid2aids[pid] for pid in pids]
    return list(chain(*aids))

def SwapPapers(fromAuthor,toAuthor,aid2pids,pid2aids,nSwaps=1):
    '''
    Move paper(s) from one author to the other
    AT MOST nSwaps swaps are performed.
    i.e. If the fromAuthor has nSwaps or less papers, he will be "cleared out"

    This is done by adjusting the aid2pids and pid2aids dicts
        
    IMPORTANT NOTES: 
    * This is performed *in-place* on aid2pids and pid2aids
    * This may result in some authors ending up with NO papers.. may need to update the author dataframe to remove "empty" authors
    '''
    
    # List of pids to swap
    swapCandidatePids=aid2pids[fromAuthor]

    try:
        swapPids=choice(swapCandidatePids,min(nSwaps,len(swapCandidatePids)),replace=False)
    except ValueError: 
        if len(swapCandidatePids)==0:
            return 1 # Failed swap, probably due to empty swapCandidate set
        else:
            raise RuntimeError("Failure to extract swapPids")
        
    for swapPid in swapPids:

        # Adjusting pid2aids
        pid2aids[swapPid].remove(fromAuthor)
        pid2aids[swapPid].append(toAuthor)
        
        # Adjusting aid2pids
        aid2pids[fromAuthor].remove(swapPid)
        aid2pids[toAuthor].append(swapPid)

    return 0 # successful completion

def GenLookupDicts(paaFile):
    '''   
    Generating the pid->aid and aid->pid lookup dicts
    (i.e. the "aid2pids" and "pid2aids" dicts required for Collabs and other functions)

    paaFile is the relevant "PaperAuthorAffiliations" file
    '''
    
    df=pd.read_csv(paaFile,'\t',names=['pid','aid','affid','oaffid','naffid','asn'])

    foo=df[['pid','aid']].groupby('aid')['pid'].apply(lambda tmp: '["'+'","'.join(tmp)+'"]')
    aid2pids=dict(zip(foo.index,[eval(foo[tmp]) for tmp in foo.index]))

    foo=df[['aid','pid']].groupby('pid')['aid'].apply(lambda tmp: '["'+'","'.join(tmp)+'"]')
    pid2aids=dict(zip(foo.index,[eval(foo[tmp]) for tmp in foo.index]))

    return aid2pids,pid2aids

def Aid2Affil(paaFile):

    df=pd.read_csv(paaFile,'\t',names=['aid','affid'],usecols=[1,2]).dropna()
    return dict(df.values)

def FiltPid2Aids(pid2aids,aidList):
    '''
    processes the pid2aids structure
    leaving only valid authors (i.e. those in aidList)
    '''

    permitted=set(aidList)
    foo=[(tmp[0],list(permitted.intersection(tmp[1]))) for tmp in pid2aids.items()]
    return {tmp[0]:tmp[1] for tmp in foo if len(tmp[1])>0}

def FiltAid2Pids(aid2pids,aidList):
    '''
    processes the aid2pids structure
    leaving only valid authors (i.e. those in aidList)
    '''
             
    permitted=set(aidList)
    return { tmp[0]:tmp[1] for tmp in aid2pids.items() if tmp[0] in permitted }

