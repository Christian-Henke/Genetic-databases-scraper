# this will require a few pip installs:
#pip3 install requests
#pip install pandas
#run with command: python genelabScraper.py
# so obviously you'll need python as well, or use Jupyter

import requests #reading web pages
import sys #make system calls
import json #reading json
import csv #outputting csv
import pandas as pd #converting to dataframes
#from collections import MutableMapping 
from itertools import chain,starmap #for flattening 
import os #for folder making

# flatten nested JSON iteratively, code from 
#https://towardsdatascience.com/how-to-flatten-deeply-nested-json-objects-in-non-recursive-elegant-python-55f96533103d
def convert_flatten(dictionary):
    """Flatten a nested json file"""
    def unpack(parent_key, parent_value):
        """Unpack one level of nesting in json file"""
        # Unpack one level only!!!
        if isinstance(parent_value, dict):
            for key, value in parent_value.items():
                temp1 = parent_key + '_' + key
                yield temp1, value
        elif isinstance(parent_value, list):
            i = 0 
            for value in parent_value:
                temp2 = parent_key + '_'+str(i) 
                i += 1
                yield temp2, value
        else:
            yield parent_key, parent_value                
    # Keep iterating until the termination condition is satisfied
    while True:
        # Keep unpacking the json file until all values are atomic elements (not dictionary or list)
        dictionary = dict(chain.from_iterable(starmap(unpack, dictionary.items())))
        # Terminate condition: not any value in the json file is dictionary or list
        if not any(isinstance(value, dict) for value in dictionary.values()) and \
           not any(isinstance(value, list) for value in dictionary.values()):
            break
    return dictionary

try:
        #Genelab data
        print("Genelab data (will take a long while)")
        print("using url")
        # if max retries used up for url, add or remove a 0 from 10000
        url = 'https://genelab-data.ndc.nasa.gov/genelab/data/glds/files/1-10000'
        print(url)
        # query the website and return to the variable 'page'
        page = requests.get(url)
        data = page.json()
        data = convert_flatten(data)
        data = json.dumps(data, indent=4) #dict into string
        #print(data)
        #input("Enter to continue")
        
        # go through all GLDS items
        gldsStudy = []
        gldsStudy.append(['Number','Data','Metadata'])
        miss = 0
        totalItems = 1
        x = 1
        path = os.path.join(os.getcwd(), "All GLDS items");
        #print("Path: " + path)
        if not os.path.exists(path):
            os.makedirs(path)
        while True:
                item = '"' + str(x) + '"'
                if (data.find(item)==-1):
                        miss = miss+1
                else:
                        url = 'https://genelab-data.ndc.nasa.gov/genelab/data/glds/files/'+str(x)
                        page = requests.get(url)
                        gldsdata = page.json()
                        # /meta/ url no longer works the same way
                        #url = 'https://genelab-data.ndc.nasa.gov/genelab/data/glds/meta/'+str(x)
                        #page = requests.get(url)
                        #gldsmetadata = page.json()
                        gldsStudy.append([x, gldsdata]) #, gldsmetadata])
                        gldsdata = convert_flatten(gldsdata)
                        tempWriter = csv.writer(open(os.path.join(path,"GLDS"+str(x)+".csv"), 'w', encoding='utf-8'), lineterminator = '\n')
                        for key in gldsdata.keys():
                                tempWriter.writerow([key,gldsdata[key]])
                        #gldsmetadata = convert_flatten(gldsmetadata)
                        #tempWriter = csv.writer(open(os.path.join(path,"MetaGLDS"+str(x)+".csv"), 'w', encoding='utf-8'), lineterminator = '\n')
                        #for key in gldsmetadata.keys():
                        #        tempWriter.writerow([key,gldsmetadata[key]])
                        totalItems = x
                if (miss>=300): #300 for safety, 50 probably fine
                        break
                x = x+1
        print("Highest GLDS study found: " + str(totalItems))

        #with open("GLDSallData.csv","w", encoding='utf-8') as f:
        #        write = csv.writer(f)
        #        write.writerows(gldsStudy)

        #print(gldsStudy[1])
        #input("Enter to continue")

        print("MGnify API Json files ")
        print("using url")
        url = 'https://www.ebi.ac.uk/metagenomics/api/v1/analyses'
        print(url)
        # query the website and return to the variable 'page'
        page = requests.get(url)
        data = page.json()
        data = convert_flatten(data)
        tempWriter = csv.writer(open("MGnify Analyses.csv", 'w', encoding='utf-8'), lineterminator = '\n')
        for key in data.keys():
                tempWriter.writerow([key,data[key]])
        #data = json.dumps(data, indent=4) #dict into string
	#print(data)
        #input("Enter to continue")
        
        #with open("MGnify Analyses.txt","w", encoding='utf-8') as f:
        #        f.write(data)

        print("using url")
        url = 'https://www.ebi.ac.uk/metagenomics/api/v1/genomes'
        print(url)
        # query the website and return to the variable 'page'
        page = requests.get(url)
        data = page.json()
        data = convert_flatten(data)
        tempWriter = csv.writer(open("MGnify Genomes.csv", 'w', encoding='utf-8'), lineterminator = '\n')
        for key in data.keys():
                tempWriter.writerow([key,data[key]])
        #data = json.dumps(data, indent=4) #dict into string
        #print(data)
        #input("Enter to continue")
        
        #with open("MGnify Genomes.txt","w", encoding='utf-8') as f:
        #        f.write(data)

        print("using url")
        url = 'https://www.ebi.ac.uk/metagenomics/api/v1/genomeset'
        print(url)
        # query the website and return to the variable 'page'
        page = requests.get(url)
        data = page.json()
        data = convert_flatten(data)
        tempWriter = csv.writer(open("MGnify Genomeset.csv", 'w', encoding='utf-8'), lineterminator = '\n')
        for key in data.keys():
                tempWriter.writerow([key,data[key]])
        #data = json.dumps(data, indent=4) #dict into string
        #print(data)
        #input("Enter to continue")
        
        #with open("MGnify Genomeset.txt","w", encoding='utf-8') as f:
        #        f.write(data)


        print("using url")
        url = 'https://www.ebi.ac.uk/metagenomics/api/v1/studies'
        print(url)
        # query the website and return to the variable 'page'
        page = requests.get(url)
        data = page.json()
        data = convert_flatten(data)
        tempWriter = csv.writer(open("MGnify Studies.csv", 'w', encoding='utf-8'), lineterminator = '\n')
        for key in data.keys():
                tempWriter.writerow([key,data[key]])
        #data = json.dumps(data, indent=4) #dict into string
        #print(data)
        #input("Enter to continue")
        
        #with open("MGnify Studies.txt","w", encoding='utf-8') as f:
        #        f.write(data)

        print("using url")
        url = 'https://www.ebi.ac.uk/metagenomics/api/v1/super-studies'
        print(url)
        # query the website and return to the variable 'page'
        page = requests.get(url)
        data = page.json()
        data = convert_flatten(data)
        tempWriter = csv.writer(open("MGnify Super-Studies.csv", 'w', encoding='utf-8'), lineterminator = '\n')
        for key in data.keys():
                tempWriter.writerow([key,data[key]])
        #data = json.dumps(data, indent=4) #dict into string
        #print(data)
        #input("Enter to continue")
        
        #with open("MGnify Super-Studies.txt","w", encoding='utf-8') as f:
        #        f.write(data)

        print("using url")
        url = 'http://biokb.ncpsb.org.cn/RadAtlas/Public/file/IR_associated_genes+evidence.json'
        print(url)
        # query the website and return to the variable 'page'
        page = requests.get(url)
        data = page.json()
        data = convert_flatten(data)
        tempWriter = csv.writer(open("RadAtlas IR_associated_genes+evidence.csv", 'w', encoding='utf-8'), lineterminator = '\n')
        for key in data.keys():
                tempWriter.writerow([key,data[key]])
        #data = json.dumps(data, indent=4) #dict into string
        #print(data)
        #input("Enter to continue")
        
        #with open("RadAtlas IR_associated_genes+evidence.txt","w", encoding='utf-8') as f:
        #        f.write(data)



        # Without requests we would use pycurl to do a curl request
        #curl -X GET "https://www.ebi.ac.uk/metagenomics/api/latest/"

        

except Exception as e:
	print("Some exception happened")
	print(type(e))
	#print(e.reason)
	#print(e.args)
	print(e)


sys.exit()

