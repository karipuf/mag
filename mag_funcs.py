from numpy import log
import numpy

# Adapted from ygraph tagsfile_directional_distmat function
# kwdict is a file which links each keyword to the doc/context in which it appears
def DirectionalDistmat(kwlist,kwdict,debug=0,largenumber=None):

    # If zero occurrences, use this as a minimum value
    min_occurrences=0.5

    # Preparing the data
    #kwdict=pickle.load(open(picklefile))
    if largenumber==None:
        kws=100000 # Just pick a large number
    else:
        kws=largenumber

    # Creating the term occurrence matrix
    n=dict()
    n12=dict()
    for kw1 in kwlist:
        n[kw1]=max(min_occurrences,len(kwdict[kw1]))
        for kw2 in kwlist:
            try: 
                intercount=max(min_occurrences,len(set(kwdict[kw1]).intersection(kwdict[kw2])))
            except KeyError:
                pdb.set_trace()
            n12[kw1,kw2]=intercount
            n12[kw2,kw1]=intercount   
    
    # Creating the distance matrix
    distmat=numpy.zeros([len(kwlist),len(kwlist)])
    for count1 in range(len(kwlist)):
        kw1=kwlist[count1]
        tmpcount1=n[kw1]
        for count2 in range(len(kwlist)):    
            kw2=kwlist[count2]
            try:
                tmpcount12=n12[kw1,kw2]
            except KeyError:
                tmpcount12=0.5
            tmpcount2=n[kw2]
            distmat[count1,count2]=(log(tmpcount1)-log(tmpcount12))/(log(kws)-log(tmpcount2))
    
    if debug:
        return [distmat,n,n12]
    else:
        return distmat
        #return yir.yir_approximate_distmat(distmat.clip(0,1)); # Let's see...
