
# if brand highlighted get 5 random samples from just that msa
# read ps-comp and get highlighted brands

import json
from multiprocessing.sharedctypes import Value
from re import L
import pandas as pd
import random as r
import itertools
from anytree import Node, RenderTree
from operator import itemgetter

sampleDataCompare = [] # Create empty list in which to put PropertyName and MSA of sample data
sampleData = {} # Create empty data dictionary
lst = []

# Load master list into a list of dictionaries
f = open('CompetitorList.json')
masterDict = json.load(f)

df = pd.read_csv('Selection-Criteria.csv', encoding='windows-1252') # Open a csv pandas csv reader
sampleData = df.to_dict('records') # Turn pandas csv data into a list of dictionaries
  
#---------------------------------------------------------------------------------------------------#
#  We're creating a large list in which each entry is a list containing PropertyName and MSA. This  #
#  allows us to iterate over the indices and compare these values to the keys in the masterDict and #
#  then run our function to get the random sample.                                                  #
#---------------------------------------------------------------------------------------------------#

for dic in sampleData: # Iterate through list of dictionaries in sampleData list
    sd = [dic[key] for key in dic if key == "PropertyName" or key == "MSA"] # Create list that contains [PropertyName, MSA]
    sampleDataCompare.append(sd) # Nest [PropertyName, MSA] in larger list

sampleDataCompare.sort()

for dic in masterDict: # Iterate over entries in the master-list
    for i in range(len(sampleDataCompare)): # Check the key's value(MSA) against the list of sampleData values for every sample entry
        if dic["MSA"] == sampleDataCompare[i][1] and dic["PropertyName"] == sampleDataCompare[i][0]: # Compare key to the MSA value in the 
            # d = {"MSA":dic["MSA"], "PropertyName":sampleDataCompare[i][0], "Address":dic["Address"]}
            str1 = list(dic["MSA"])
            str2 = list(dic["PropertyName"])
            str3 = list(dic["Address"])
            l = []
            if dic["MSA"] and dic["PropertyName"] not in lst:
                l.append(str1)
                l.append(str2)
                l.append(str3)
                lst.append(l)
            else:
                res = lst.index(dic["MSA"])
                l.append()
                lst[res][0][0].append(str3)
        else:
            continue


    


# sortedlst = sorted(lst, key=itemgetter("MSA")) # Sort list alphabetically by MSA Value

with open('output-file.json', 'w') as fout:
    json.dump(lst, fout)
