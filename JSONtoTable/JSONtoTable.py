# this will require a few pip installs:
#pip3 install requests requests
#run with command: python JSONtoTable.py
# so obviously you'll need python as well, or use Jupyter

import requests #reading web pages
import sys #make system calls, get command arguments
import json #reading json
import csv #outputting csv
#from collections import MutableMapping 
from itertools import chain,starmap #for flattening 
import pandas

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



#tested with: 
#python JSONtoTable.py "C:\Users\chris\Downloads\MGnify Analyses.txt" flattenedJSON.txt 
# can be saved into other formats

try:
        #print('Number of arguments:', len(sys.argv), 'arguments.')
        #print('Argument List:'+str(sys.argv))
        print("Input file: ",str(sys.argv[1]))
        print("Output file: ",str(sys.argv[2]))

        with open(sys.argv[1], "r") as f:
                data = json.load(f)
        data = convert_flatten(data)        
        data = json.dumps(data, indent=4) #dict into string
        with open(sys.argv[2],"w+", encoding='utf-8') as f: #create file if it doesn't exist
                f.write(data)
        
        sys.exit() # below is testing using website json
        
        print("using url")
        url = 'https://www.ebi.ac.uk/metagenomics/api/v1/analyses'
        print(url)
        # query the website and return to the variable 'page'
        page = requests.get(url)
        data = page.json()

        with open("JSON.json","w", encoding='utf-8') as f:
                f.write(json.dumps(data, indent=4))
        
        data = convert_flatten(data)
        with open("flattened JSON.csv", 'w', encoding='utf-8') as f:
                for key in data.keys():
                        f.write("%s,%s\n"%(key,data[key]))

        data = json.dumps(data, indent=4) #dict into string
        with open("flattened JSON.txt","w", encoding='utf-8') as f:
                f.write(data)
        
        

except Exception as e:
	print("Some exception happened")
	print(type(e))
	#print(e.reason)
	#print(e.args)
	print(e)


sys.exit()

