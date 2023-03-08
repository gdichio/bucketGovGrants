#%%
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
from selenium.webdriver.common.by import By
import time
from tqdm import tqdm
from src.Grants import getGrant
#%%
driver = webdriver.Chrome(executable_path="/gianyrox1/opt/anaconda3/lib/python3.9/site-packages")
driver.implicitly_wait(10)

oppIds = pd.read_csv('//Users//gianyrox1//bucket_projects//web-s//bucketGovGrants//OppIDs.csv', index=False)
#%%

ID = "oppId=344165"

#oppIDString = "OppID" + str(oppID)

driver.get(f"https://www.grants.gov/custom/viewOppDetails.jsp?{ID}")
driver.execute_script("document.body.style.zoom='20%'")
#%%
#check if ID is a grant
ID_check = driver.find_element(By.ID, 'loadingDataMsg')
#if str(ID_check.text) == "There is no record found for your search.": 
#    continue;

#%%
data = ''
for i in synopsis:
    data = i.text
pairs = data.split('\n')

STOPS = ['Print Synopsis Details','?','General Information','Eligibility', 'Additional Information']
for stop in STOPS:
    if stop in pairs:
        pairs.remove(stop)

#dict for each oppID
OppDict = {}
#%%
"""for value in pairs:
    if ':' in value:
        a = value.split(':')
        key = a[0]
        val = a[1]
        OppDict[key] = val
        OppDict[key] = [OppDict[key]]
    else:         
        OppDict[key].append(value)

generalInfo = {}
generalInfoTypes = ['Document Type', 'Funding Opportunity Number', 'Funding Opportunity Title', 'Opportunity Category', 
'Opportunity Category Explanation', 'Funding Instrument Type', 'Category of Funding Activity', 'Category Explanation', 
'Expected Number of Awards', 'CFDA Number(s)', 'Cost Sharing or Matching Requirement', 'Version', 'Posted Date', 'Last Updated Date', 
'Original Closing Date for Applications', 'Current Closing Date for Applications', 'Archive Date', 'Estimated Total Program Funding', 
'Award Ceiling', 'Award Floor']


for key in OppDict:
    if key in generalInfoTypes:
        generalInfo[key] = OppDict[key]

#locals()['oppIDString'] = Grant(generalInfo[key] for key in generalInfo)

oppIDs.append(oppIDString)

    return oppIDs, fullIDs, nullIDs
"""

#%%

OppDF = DataFrame()

oppId = 345146

opp = DataFrame(getGrant(oppId))

#%%
for key in opp:
    print (opp[key])
#%%

def oppCleaning(opp):
    for key in opp:
        if "Date" in key:
            opp[key] = 
        if 
#%%

Opportunity = oppCleaning(opp)

OppDF = pd.concat([OppDF,Opportunity], ignore_index=True)
OppDF.to_csv('//Users//gianyrox1//bucket_projects//bucketGovGrants//OppDF.csv', index=False)
    
df = pd.read_csv('//Users//gianyrox1//bucket_projects//bucketGovGrants//OppDF.csv', index=False)
