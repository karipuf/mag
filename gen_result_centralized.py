import pandas as pd
import os

finalres=[]

print
print "KDD Cup"
print "-------"
os.chdir('2016KDDCupSelected')
execfile('gen_results.py')
finalres.append((homogcount,mainlyhomogcount,randomhomogcount,randommainlyhomogcount))

print
print "Sustainable Energy"
print "------------------"
os.chdir('../SustainableEnergy')
execfile('gen_results.py')
finalres.append((homogcount,mainlyhomogcount,randomhomogcount,randommainlyhomogcount))

print
print "Mechanical Engineering"
print "-----------------------"
os.chdir('../MechanicalEngineering')
execfile('gen_results.py')
finalres.append((homogcount,mainlyhomogcount,randomhomogcount,randommainlyhomogcount))

print
print "Cardiology"
print "-----------------------"
os.chdir('../Cardiology')
execfile('gen_results.py')
finalres.append((homogcount,mainlyhomogcount,randomhomogcount,randommainlyhomogcount))


os.chdir('..')
finalres=pd.DataFrame(finalres)
finalres.columns=['#Homogeneous','#Mainly-Homogeneous','#Randomized homogeneous','#Randomized mostly homogeneous']
finalres.index=['KDD','Sustainable Energy','Mechanical Engineering','Cardiology']
