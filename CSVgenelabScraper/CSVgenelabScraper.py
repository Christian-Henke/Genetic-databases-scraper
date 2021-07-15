# this will require a few pip installs:
#pip3 install pandas
#run with command: python CSVgenelabScraper.py
# so obviously you'll need python as well, or use Jupyter

import requests #reading web pages
import sys #make system calls, get command arguments
import json #reading json
import csv #outputting csv
import pandas as pd #for json to csv
from pandas import json_normalize #same reason
from copy import deepcopy #same reason
import os #for making folders

#first init
multi = []; inner = {}

#recursively extract json data into dataframe
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



#load JSONs, convert to CSV, output CSV
#conversion:
#df = extract(data)
#df.to_csv('Output.csv')
try:
        #Genelab data
        print("Genelab data (will take a long while)")
        print("using url")
        url = 'https://genelab-data.ndc.nasa.gov/genelab/data/glds/files/1-1000'
        print(url)
        # query the website and return to the variable 'page'
        page = requests.get(url)
        findData = page.json()
        findData = json.dumps(findData, indent=4) #dict into string
        #print(data)
        #input("Enter to continue")
        
        # go through all GLDS items
        miss = 0
        totalItems = 1
        x = 1
        path = os.path.join(os.getcwd(), "All GLDS items");
        #print("Path: " + path)
        if not os.path.exists(path):
            os.makedirs(path)
        while True:
                item = '"' + str(x) + '"'
                if (findData.find(item)==-1):
                        miss = miss+1
                else:
                        url = 'https://genelab-data.ndc.nasa.gov/genelab/data/glds/files/'+str(x)
                        page = requests.get(url)
                        gldsdata = page.json()
                        #df = extract(gldsdata)
                        #fieldnames = set()
                        #for entry in gldsdata:
                        #        fieldnames.update(get_leaves(entry).keys)
                        #csv_output = csv.DictWriter(open(os.path.join(path,'GLDS'+str(x)+'.json'),"w", encoding='utf-8'), fieldnames=sorted(fieldnames))
                        #csv_output.writeheader()
                        #csv_output.writerows(get_leaves(entry) for entry in gldsdata)
			#df = json_normalize(gldsdata,max_level=None)
                        #df.to_csv(os.path.join(path,'GLDS'+str(x)+'.csv'), index=False)
                        with open(os.path.join(path,'GLDS'+str(x)+'.json'),"w", encoding='utf-8') as f:
                                json.dump(gldsdata,f,indent=4)

                        # /meta/ url no longer works the same way
                        #url = 'https://genelab-data.ndc.nasa.gov/genelab/data/glds/meta/'+str(x)
                        #page = requests.get(url)
                        #gldsmetadata = page.json()
                        #fieldnames = set()
                        #for entry in gldsmetadata:
                        #        fieldnames.update(get_leaves(entry).keys())
                        #csv_output = csv.DictWriter(open(os.path.join(path,'GLDS'+str(x)+'.json'),"w", encoding='utf-8'), fieldnames=sorted(fieldnames))
                        #csv_output.writeheader()
                        #csv_output.writerows(get_leaves(entry) for entry in gldsmetadata)
                        #df = extract(gldsmetadata)
                        #df = json_normalize(gldsmetadata,max_level=None)
                        #df.to_csv(os.path.join(path,'MetaGLDS'+str(x)+'.csv'), index=False)
                        #with open(os.path.join(path,'metaGLDS'+str(x)+'.json'),"w", encoding='utf-8') as f:
                        #       json.dump(gldsmetadata,f,indent=4)
                        totalItems = x
                        #input("check")
                if (miss>=300): #300 for safety, 50 probably fine
                        break
                x = x+1
        print("Highest GLDS study found: " + str(totalItems))

        

        #print(gldsStudy[1])
        #input("Enter to continue")


        print("MGnify API Json files ")
        print("using url")
        url = 'https://www.ebi.ac.uk/metagenomics/api/v1/analyses'
        print(url)
        # query the website and return to the variable 'page'
        page = requests.get(url)
        data = page.json()
        df = extract(data)
        df.to_csv('MGnify Analyses.csv')
        #print(data)
        #input("Enter to continue")
        
        print("using url")
        url = 'https://www.ebi.ac.uk/metagenomics/api/v1/genomes'
        print(url)
        # query the website and return to the variable 'page'
        page = requests.get(url)
        data = page.json()
        df = extract(data)
        df.to_csv('MGnify Genomes.csv')
        #print(data)
        #input("Enter to continue")
        
        print("using url")
        url = 'https://www.ebi.ac.uk/metagenomics/api/v1/genomeset'
        print(url)
        # query the website and return to the variable 'page'
        page = requests.get(url)
        data = page.json()
        df = extract(data)
        df.to_csv('MGnify Genomeset.csv')
        

        print("using url")
        url = 'https://www.ebi.ac.uk/metagenomics/api/v1/studies'
        print(url)
        # query the website and return to the variable 'page'
        page = requests.get(url)
        data = page.json()
        df = extract(data)
        df.to_csv('MGnify Studies.csv')
        #print(data)
        #input("Enter to continue")
        
        print("using url")
        url = 'https://www.ebi.ac.uk/metagenomics/api/v1/super-studies'
        print(url)
        # query the website and return to the variable 'page'
        page = requests.get(url)
        data = page.json()
        df = extract(data)
        df.to_csv('MGnify Super-Studies.csv')
        #print(data)
        #input("Enter to continue")

        print("using url")
        url = 'http://biokb.ncpsb.org.cn/RadAtlas/Public/file/IR_associated_genes+evidence.json'
        print(url)
        # query the website and return to the variable 'page'
        page = requests.get(url)
        data = page.json()
        df = extract(data)
        df.to_csv('RadAtlas IR_associated_genes+evidence.csv')
        #print(data)
        #input("Enter to continue")
        


        

      

        # Without requests we would use pycurl to do a curl request
        #curl -X GET "https://www.ebi.ac.uk/metagenomics/api/latest/"

        

except Exception as e:
	print("Some exception happened")
	print(type(e))
	#print(e.reason)
	#print(e.args)
	print(e)


sys.exit()
