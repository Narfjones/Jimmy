
# if brand highlighted get 5 random samples from just that msa
# read ps-comp and get highlighted brands

import json
from multiprocessing.sharedctypes import Value
from re import L
import pandas as pd
import random as r

sampleDataCompare = [] # Create empty list in which to put PropertyName and MSA of sample data
sampleData = {} # Create empty data dictionary
lst = []

# Load master list into a list of dictionaries
f = open('CompetitorList.json')
masterDict = json.load(f)

df = pd.read_csv('Selection-Criteria.csv') # Open a csv pandas csv reader
sampleData = df.to_dict('records') # Turn pandas csv data into a list of dictionaries
  
#---------------------------------------------------------------------------------------------------#
#  We're creating a large list in which each entry is a list containing PropertyName and MSA. This  #
#  allows us to iterate over the indices and compare these values to the keys in the masterDict and #
#  then run our function to get the random sample.                                                  #
#---------------------------------------------------------------------------------------------------#

for dic in sampleData: # Iterate through list of dictionaries in sampleData list
    sd = [dic[key] for key in dic if key == "PropertyName" or key == "MSA"] # Create list that contains [PropertyName, MSA]
    sampleDataCompare.append(sd) # Nest [PropertyName, MSA] in larger list

for dic in masterDict: # Iterate over entries in the master-list
    for key in dic: # stop at each dictionary and check the keys
        for i in range(len(sampleDataCompare)): # Check the key's value(MSA) against the list of sampleData values for every sample entry
            if dic[key] == sampleDataCompare[i][1] and dic["PropertyName"] == sampleDataCompare[i][0]: # Compare key to the MSA value in the 
                d = {"MSA":dic[key], "PropertyName":sampleDataCompare[i][0], "Address":dic['Address']}
                lst.append(d) # If they match, send the property name and msa value to the function
            else:
                continue
            
with open('output-file.json', 'w') as fout:
    json.dump(lst, fout)
