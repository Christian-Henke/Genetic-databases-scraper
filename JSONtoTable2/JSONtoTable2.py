# this will require a few pip installs:
#pip3 install pandas
#run with command: python JSONtoTable2.py
# so obviously you'll need python as well, or use Jupyter

import requests #reading web pages
import sys #make system calls, get command arguments
import json #reading json
import csv #outputting csv
import pandas as pd

#first init
multi = []; inner = {}

def extract(d):
    global multi, inner
    multi = []; inner = {}
    def recursive_extract(i):
        global multi, inner

        if type(i) is list:
            if len(i) == 1:
                for k,v in i[0].items():
                    if type(v) in [list, dict]:
                        recursive_extract(v)
                    else:                
                        inner[k] = v
            else:
                multi = i

        if type(i) is dict:
            for k,v in i.items():
                if type(v) in [list, dict]:
                    recursive_extract(v)
                else:                
                    inner[k] = v
    recursive_extract(d)

    data_dict = []
    for i in multi:    
        tmp = inner.copy()
        tmp.update(i)
        data_dict.append(tmp)

    df = pd.DataFrame(data_dict)
    return df

#tested with: 
#python JSONtoTable2.py "C:\Users\chris\Downloads\MGnify Analyses.txt" flattenedJSON.txt 
# can be converted to other formats besides .txt

try:
        #print 'Number of arguments:', len(sys.argv), 'arguments.'
        #print('Argument List:'+str(sys.argv))
        print("Input file: ",str(sys.argv[1]))
        print("Output file: ",str(sys.argv[2]))

        with open(sys.argv[1], "r") as f:
                data = json.load(f)
        
        df = extract(data)
        df.to_csv(sys.argv[2])
        
        sys.exit() # below is testing using website json
        
        print("using url")
        url = 'https://www.ebi.ac.uk/metagenomics/api/v1/analyses'
        print(url)
        # query the website and return to the variable 'page'
        page = requests.get(url)
        data = page.json()

        with open("JSON.json","w", encoding='utf-8') as f:
                f.write(json.dumps(data, indent=4))
        
        df = extract(data)
        df.to_csv("Extracted JSON.csv")       
        

except Exception as e:
	print("Some exception happened")
	print(type(e))
	#print(e.reason)
	#print(e.args)
	print(e)


sys.exit()

