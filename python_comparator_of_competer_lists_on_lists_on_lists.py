
# if brand highlighted get 5 random samples from just that msa
# read ps-comp and get highlighted brands

import json
import pandas as pd
import random as r
from collections import defaultdict

sampleDataCompare = [] # Create empty list in which to put PropertyName and MSA of sample data
sampleData = {} # Create empty data dictionary
lst = [] # This is the final output
lst_msa = [] # Tracker for which msas we have already written
lst_prop_name = [] # Tracker for which properties we've already written

# Load master list into a list of dictionaries
f = open('CompetitorList.json')
masterDict = json.load(f)

for dic in masterDict: # Combine city, state, zip into address
    dic['Address'] = str(dic["Address"] + " " + dic["city"] + " " + dic["State"] + " " + str(dic["Zipcode"]))


df = pd.read_csv('Selection-Criteria.csv', encoding='windows-1252') # Open a pandas csv reader
sampleData = df.to_dict('records') # Turn pandas csv data into a list of dictionaries

#---------------------------------------------------------------------------------------------------#
#  We're creating a large list in which each entry is a list containing PropertyName and MSA. This  #
#  allows us to iterate over the indices and compare these values to the keys in the masterDict and #
#  then run our function to get the random sample.                                                  #
#---------------------------------------------------------------------------------------------------#

for dic in sampleData: # Iterate through list of dictionaries in sampleData list
    sd = [dic[key] for key in dic if key == "MSA" or key == "PropertyName"] # Create list that contains [PropertyName, MSA]
    sampleDataCompare.append(sd) # Nest [PropertyName, MSA] in larger list

with open('sample_data_compare.json', 'w') as fout: # This allows you to easily check the sampleData and structure without printing stuff.
    json.dump(sampleDataCompare, fout)

def compile_lst():
    r.shuffle(masterDict) # Shuffle the order of dictionaries
    for dic in masterDict: # Iterate over entries in the master-list
        # Resets PropertyName after each dictionary so that it can grad the same property from different MSAs

        ls_prop_name = [] # This is a misspelling but if you correct it the whole thin breaks

        for i in range(len(sampleDataCompare)): # Check the key's value(MSA) against the list of sampleData values for every sample entry
            if dic["MSA"] == sampleDataCompare[i][1] and dic["PropertyName"] == sampleDataCompare[i][0]: # Compare key to the MSA value in the list
               
                # Instead of creating a new dictionary, we are creating nested lists. So, instead of setting values equal we
                # save the dictionary values as strings, append them to a list, and then append that list to the output
                str1 = str(dic["MSA"])
                str2 = str(dic["PropertyName"])
                str3 = str(dic["Address"])
                l1 = []
                l2 = []
                l3 = []

                # If MSA hasn't been accessed yet, we create a new entry
                if dic["MSA"] not in lst_msa: 
                    lst_msa.append(dic["MSA"])
                    lst_prop_name.append(dic["PropertyName"])
                    l1.append(str1)
                    l2.append(str2)
                    l3.append(str3)
                    lst.append(l1)
                    for j in lst:
                        if j == l1:
                            j.append(l2)
                        for k in j:
                            if k == l2:
                                k.append(l3)

                # If the MSA is there but the property hasn't been accessed we append it instead of making a copy of the MSA
                elif str1 in lst_msa and str2 not in lst_prop_name: 
                        lst_prop_name.append(dic["PropertyName"])
                        l1.append(str1)
                        l2.append(str2)
                        l3.append(str3)
                        for j in lst:
                            for k in j:
                                if k == str1 and l2 not in j:
                                    j.append(l2)
                            for t in j:
                                for u in t:
                                    if u == str2 and l3 not in t:
                                        t.append(l3)  

                # If the MSA and Property have both been matched before we simply append the address              
                else:
                    l1.append(str1)
                    l2.append(str2)
                    l3.append(str3)
                    for m in lst:
                        for n in m:
                            for o in n:
                                if str1 in m and str2 in n and str3 not in o and o != str2:
                                    if len(o) < 5: # Stops writing after 5 entries. Lists are unordered so this should give random results.
                                        o.append(str3)
            else:
                continue
                
compile_lst()

with open('output-file.json', 'w') as fout:
    json.dump(lst, fout)

