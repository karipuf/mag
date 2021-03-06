import pandas as pd
import pylab as pl
import numpy as np
import pickle,re
from ethnicity_funcs import name2ethnicity
from disambig_funcs import Collabs,GenLookupDicts,SwapPapers,Gini
from itertools import chain
from copy import deepcopy
from numpy.random import choice
from scipy.stats import pearsonr

###########
# Set-up
###########

# Number of author pairs to perform the swap for
nSwapPairs=6320 # 10%!!
nSwapPapers=1 # Papers to swap per author
truncreg=re.compile('^\s*(\S).*?(\s{0,1}\S+)\s*$')
ethDict=pickle.load(open("ethnicitiesMech.pkl",'rb'))
np.random.seed(10)

###################################
# Preparing the data
##################################

print("Loading and prepping data...")

aid2pids,pid2aids=GenLookupDicts('MechanicalEngineeringSelectedPaperAuthorAffiliations.txt')

# Processing author file
au=pd.read_csv("MechanicalEngineeringSelectedAuthors.txt",'\t',names=['aid','name'])
au['trunc']=au['name'].apply(lambda tmp: ''.join(truncreg.findall(tmp)[0]))
au['eth']=au['name'].apply(lambda tmp: name2ethnicity(tmp,ethDict))
aideth=au[['aid','eth']].set_index('aid')['eth']

# Generating individual diversities for each author
au['diversity']=au['aid'].apply(lambda aid: Gini([aideth[tmp] for tmp in Collabs(aid,aid2pids,pid2aids)]))

#############################################
# Preparing the "ambiguate" the authors
#############################################

ambigsets=[eval(tmp) for tmp in au.groupby('trunc')['aid'].apply(lambda tmp: '["'+'","'.join(tmp)+'"]')]
ambigsets=[tmp for tmp in ambigsets if len(tmp)>1]

# Ambiguation!!
print('Performing the "ambiguation..."')

ambig_aid2pids=deepcopy(aid2pids)
ambig_pid2aids=deepcopy(pid2aids)
failedSwaps=[] # Record of failed swaps (due to "emptied out" authors)
for count in range(nSwapPairs):

    # Pick two random authors (with similar names) to swap
    swapset=choice(ambigsets)
    fromAuthor,toAuthor=choice(swapset,2,replace=False)
                
    # Move paper(s) from first author to the other  
    failedSwaps.append(SwapPapers(fromAuthor,toAuthor,ambig_aid2pids,ambig_pid2aids))

# Generating updated diversities
print('Calculating "ambiguated" diversities')
au['ambiguateddiversity']=au['aid'].apply(lambda aid: Gini([aideth[tmp] for tmp in Collabs(aid,ambig_aid2pids,ambig_pid2aids)]))
print("Done, there were "+str(sum(failedSwaps))+" failed swaps")


# List of "non-zeroed" authors
nonzero=[tmp for tmp in ambig_aid2pids.keys() if len(ambig_aid2pids[tmp])>0]
aud=au[au.aid.isin(nonzero)]

# Generating plots outputs
print("R for original vs ambiguated is "+str(pearsonr(aud.diversity,aud.ambiguateddiversity)[0]))
print()
print("Plotting results for "+str(nSwapPairs)+" swaps...")
cumulDiv,x1,foo=pl.hist(aud.diversity.values.reshape((-1,1)),bins=20,cumulative=True,density=True)
cumulDivAmbiguated,x2,foo=pl.hist(aud.ambiguateddiversity.values.reshape((-1,1)),bins=x1,cumulative=True,density=True)

pl.close()

pl.subplot(1,2,1)
pl.title("CDF - ethnic diversity")
pl.plot(x1[:-1],cumulDiv)
pl.plot(x2[:-1],cumulDivAmbiguated,'--')
pl.legend(["Original","Ambiguated"])
pl.ylabel("CDF")
pl.xlabel("$d_{eth}^I$")

pl.subplot(1,2,2)
pl.title('(Ethnic) Diversity vs "Ambiguated" diversity')
pl.plot(aud.diversity,aud.ambiguateddiversity,'.')
pl.ylabel("$d_{eth}^I$ (ambiguated)")
pl.xlabel("$d_{eth}^I$")

pl.show()
