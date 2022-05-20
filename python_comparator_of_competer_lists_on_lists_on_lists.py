
# if brand highlighted get 5 random samples from just that msa
# read ps-comp and get highlighted brands

import json
import pandas as pd
import random as r
from collections import defaultdict

sampleDataCompare = [] # Create empty list in which to put PropertyName and MSA of sample data
sampleData = {} # Create empty data dictionary
lst = []
lst_msa = []
lst_prop_name = []

# Load master list into a list of dictionaries
f = open('CompetitorList.json')
masterDict = json.load(f)

for dic in masterDict:
    dic['Address'] = str(dic["Address"] + " " + dic["city"] + " " + dic["State"] + " " + str(dic["Zipcode"]))


df = pd.read_csv('Selection-Criteria.csv', encoding='windows-1252') # Open a csv pandas csv reader
sampleData = df.to_dict('records') # Turn pandas csv data into a list of dictionaries

#---------------------------------------------------------------------------------------------------#
#  We're creating a large list in which each entry is a list containing PropertyName and MSA. This  #
#  allows us to iterate over the indices and compare these values to the keys in the masterDict and #
#  then run our function to get the random sample.                                                  #
#---------------------------------------------------------------------------------------------------#

for dic in sampleData: # Iterate through list of dictionaries in sampleData list
    sd = [dic[key] for key in dic if key == "MSA" or key == "PropertyName"] # Create list that contains [PropertyName, MSA]
    sampleDataCompare.append(sd) # Nest [PropertyName, MSA] in larger list

# sampleDataCompare.sort()

with open('sample_data_compare.json', 'w') as fout:
    json.dump(sampleDataCompare, fout)

def compile_lst():
    for dic in masterDict: # Iterate over entries in the master-list
        # Resets PropertyName after each dictionary
        ls_prop_name = []
        for i in range(len(sampleDataCompare)): # Check the key's value(MSA) against the list of sampleData values for every sample entry
            if dic["MSA"] == sampleDataCompare[i][1] and dic["PropertyName"] == sampleDataCompare[i][0]: # Compare key to the MSA value in the list
                # d = {"MSA":dic["MSA"], "PropertyName":sampleDataCompare[i][0], "Address":dic["Address"]}
                str1 = str(dic["MSA"])
                str2 = str(dic["PropertyName"])
                str3 = str(dic["Address"])
                l1 = []
                l2 = []
                l3 = []
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
                else:
                    l1.append(str1)
                    l2.append(str2)
                    l3.append(str3)
                    for m in lst:
                        for n in m:
                            for o in n:
                                if str1 in m and str2 in n and str3 not in o and o != str2:
                                    o.append(str3)
            else:
                continue

comb_lst = []

def compile_dict():
    prop_lst = []
    msa_lst = []
    for samp in sampleData:
        tempDic = {}
        l1 = []
        l2 = []
        for dic in masterDict: # Iterate over entries in the master-list
            
            if samp["MSA"] == dic["MSA"] and samp["PropertyName"] == dic["PropertyName"]:
                
                if dic["MSA"] not in msa_lst:
                    l = []
                    msa_lst.append(dic["MSA"])
                    prop_lst.append(dic["PropertyName"])
                    msa_lst.append(dic["MSA"])
                    
                    tempDic["MSA"] = dic["MSA"]
                    
                    l.append(dic["PropertyName"])
                    l2.append(dic["Address"])
                    
                    tempDic["Address"] = l2
                    l1.append(l)
                    l1[l1.index(dic["PropertyName"])].append(l2)
                    
                    tempDic["Properties"] = l1
                    
                    comb_lst.append(tempDic)
                    
                    if dic["PropertyName"] not in prop_lst:
                        
                        l1.append(dic["PropertyName"])
                        tempDic["Properties"] = l1
                        
                        l2.append(dic["Address"])
                        tempDic["Address"] = l2
                        
                        comb_lst.append(tempDic)
                else:
                    l2.append(dic["Address"])
                    tempDic["Address"] = l2
                    
                    comb_lst.append(tempDic)
                
compile_lst()

random_lst = {}
count_dics = 0
# for msa in lst:
#    for property in msa:
#        for address in property:
#            if type(address) == list:
#                x = len(address)
#                for i in address:
#                    if x > 5:
#                        x -= 1
#                        print(len(address))
#                    else:
#                        continue




with open('output-file.json', 'w') as fout:
    json.dump(q, fout)

