import pandas as pd
import numpy as np
import pylab as pl
import re,pickle,random,pdb

countrydict=dict(pd.read_csv("affilcountry.csv",header=None).values)

dict2ethnicity=lambda x:",".join([tmp['best'] for tmp in x])
def name2ethnicity(inname,textmapdict):
    try:
        return dict2ethnicity(textmapdict[inname])
    except:
        #return None
        return "unknown"


def last5(tmp):
    try: return tmp[-5:]
    except TypeError: return -1




# Utility data for affil2country
####################################

reg=re.compile(",\s([^,]+?)\.{0,1}$")

# Last five characters and associated countries
last5dict=dict([(', usa', 'USA'),('japan', 'Japan'),('rmany', 'Germany'),('italy', 'Italy'),('anada', 'Canada'),('ngdom', 'UK'),('china', 'China'),('apan.', 'Japan'),('weden', 'Sweden'),('nmark', 'Denmark'),('spain', 'Spain'),('ralia', 'Australia'),('ornia', 'USA'),('setts', 'USA'),('korea', 'Korea'),('esota','USA'),('a, PA','USA'),('m, NC','USA'),('n, UK','UK'),(' Ohia','USA'),('yland','USA'),('reece','Greece'),('orway','Greece'),('sreal','Israel'),('many.','Germany'),('stria','Austria'),('apan.','Japan'),('k, NY','USA'),('aiwan','Taiwan'),('o, ca','USA'),('h, pa','USA'),('i, fl','USA'),('n, tx','USA')])

# Big cities, states, etc
ukset=('london','glasgow','oxford','cambridge','birmingham','manchester','liverpool','edinburgh')
usaset=('texas','new\syork','boston','california','massachusetts','new jersey','austin','berkeley','houston','dallas','washington','seattle')
chinaset=('beijing','shanghai','guangzhou','xian')
canadaset=('toronto','waterloo','vancouver')
austset=('sydney','melbourne','nsw')
countryre=re.compile('|'.join(['('+'|'.join(tmp)+')' for tmp in (ukset,usaset,chinaset,canadaset,austset)]),re.IGNORECASE)

def affil2country(affil):

    # Cascade of methods

    # Pre-stored countries
    try:
        return countrydict[affil]
    except KeyError:
        pass

    # Last five characters
    try:
        return last5dict[last5(affil).lower()]
    except:
        pass

    # Cities, states, etc
    try:
        cvec=['UK','USA','China','Canada','Australia']
        return cvec[pl.find(countryre.search(affil).groups())[0]]
    except (AttributeError,TypeError):
        pass
    
    try:
        country=reg.search(affil).groups()[0]
        if country=="MA":
            return "USA"
        return country
    except:
        return "unknown"

def homogAnalyze(merged,numRuns=10,genFigs=False,maintainNetwork=False):
    agroups=merged.groupby('pid')
    ethnicitysets=[tmp[1].ethnicity.tolist() for tmp in iter(agroups)]

    # Testing for homogeneous sets
    ################################

    homog=lambda x:np.all([tmp==x[0] for tmp in x])
    homogs=[homog(tmp) for tmp in ethnicitysets if len(tmp)>1]

    mainlyhomog=lambda x:pd.value_counts(x).iloc[0] >= 0.75*len(x)
    mainlyhomogs=[mainlyhomog(tmp) for tmp in ethnicitysets if len(tmp)>1]

    homogcount=len(pl.find(homogs))
    mainlyhomogcount=len(pl.find(mainlyhomogs))


    # Randomly generated sets
    ############################

    random.seed(10)
    results=[]
    mainlyresults=[]

    for count in range(numRuns):

        if not maintainNetwork:
            elist=merged.ethnicity.tolist()
            random.shuffle(elist)
            randomsets=[]
            for length in [len(tmp) for tmp in ethnicitysets]:
                randomsets.append([elist.pop() for tmp in range(length)])

        else: # Shuffle in a way which maintains the overall structure of the network
            mixedauthors=np.unique(merged['aid'])
            random.shuffle(mixedauthors)
            shuffledict={mixedauthors[tmp]:mixedauthors[tmp+1] for tmp in range(0,len(mixedauthors)/2)}
            
            
            
        
                
        randomhomogs=[homog(tmp) for tmp in randomsets if len(tmp)>1]
        results.append(len(pl.find(randomhomogs)))

        randommainlyhomogs=[mainlyhomog(tmp) for tmp in randomsets if len(tmp)>1]
        mainlyresults.append(len(pl.find(randommainlyhomogs)))

        randomhomogcount=np.mean(results)
        randommainlyhomogcount=np.mean(mainlyresults)

    return homogcount,mainlyhomogcount,randomhomogcount,randommainlyhomogcount
