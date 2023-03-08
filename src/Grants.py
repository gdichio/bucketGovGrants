from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame as df
from selenium.webdriver.common.by import By
import time
from tqdm import tqdm
from selenium.webdriver.support import expected_conditions as Ey


def getGrant(oppId):

    #keys
    generalInfoTypes = [
        #'ID',
        'Document Type',
        'Funding Opportunity Number',
        'Funding Opportunity Title',
        'Opportunity Category',
        'Opportunity Category Explanation',
        'Funding Instrument Type',
        'Category of Funding Activity',
        'Category Explanation' ,
        'Expected Number of Awards' ,
        'CFDA Number(s)',
        'Cost Sharing or Matching Requirement',
        'Version',
        'Posted Date',
        'Last Updated Date',
        'Original Closing Date for Applications',
        'Current Closing Date for Applications',
        'Archive Date',
        'Estimated Total Program Funding',
        'Award Ceiling',
        'Award Floor',
        'Eligible Applicants',
        'Additional Information on Eligibility',
        'Agency Name',
        'Description',
        'Link to Additional Information',
        'Grantor Contact Information',
        ]


    #webdriver
    driver = webdriver.Safari()
    driver.implicitly_wait(10)

    #viewOpp
    ID = f"oppId={oppId}"

    driver.get(f"https://www.grants.gov/custom/viewOppDetails.jsp?{ID}")
    time.sleep(5)

    #getContent
    synopsis = driver.find_elements(By.ID, 'synopsisDetailsContent')
    data = ''
    for i in synopsis:
        data += i.text
    pairs = data


    tests = []
    for i in range(len(generalInfoTypes)):
        splits = data.split(f"{generalInfoTypes[i]}:")
        splits.insert(1,'NextValue')
        try:
            data = splits[2]
        except:pass
        tests.append(splits[0])
        tests.append(splits[1])
    tests.append(splits[2])
    tests.append(splits[1])
    tests.pop(0)
    tests.pop(0)

    STOPS = ["Print Synopsis Details","General Information","Eligibility", "Additional Information"]
    for stop in STOPS:
        for i in range(len(tests)):
            if stop in tests[i]:
                tests[i] = tests[i].replace(stop, "")

    res = []
    vals = []
    for sub in tests:
        res.append(sub.replace("\n", ""))
    for sub in res:
        vals.append(sub.replace("\t", "").strip())

    #Dictionary
    OppDict = {'ID':[oppId]}
    val = 0
    for key in range(len(generalInfoTypes)):
        OppDict[generalInfoTypes[key]] = []
        while vals[val] != 'NextValue':
            OppDict[generalInfoTypes[key]].append(vals[val])
            val += 1
        else:
            val += 1

    driver.quit()

    return OppDict


class Grant:

    """def __init__(self, Document_Type, Funding_Opportunity_Number, Funding_Opportunity_Title, Opportunity_Category, 
    Opportunity_Category_Explanation, Funding_Instrument_Type, Category_of_Funding_Activity, Category_Explanation, 
    Expected_Number_of_Awards, CFDA_Number_s, Cost_Sharing_or_Matching_Requirement, Version, Posted_Date, Last_Updated_Date, 
    Original_Closing_Date_for_Applications, Current_Closing_Date_for_Applications, Archive_Date, Estimated_Total_Program_Funding, 
    Award_Ceiling, Award_Floor):

        self.Document_Type = Document_Type 
        self.Funding_Opportunity_Number = Funding_Opportunity_Number
        self.Funding_Opportunity_Title = Funding_Opportunity_Title
        self.Opportunity_Category = Opportunity_Category 
        self.Opportunity_Category_Explanation = Opportunity_Category_Explanation
        self.Funding_Instrument_Type = Funding_Instrument_Type
        self.Category_of_Funding_Activity = Category_of_Funding_Activity
        self.Category_Explanation = Category_Explanation 
        self.Expected_Number_of_Awards = Expected_Number_of_Awards
        self.CFDA_Number_s = CFDA_Number_s
        self.Cost_Sharing_or_Matching_Requirement = Cost_Sharing_or_Matching_Requirement
        self.Version = Version
        self.Posted_Date = Posted_Date
        self.Last_Updated_Date = Last_Updated_Date 
        self.Original_Closing_Date_for_Applications = Original_Closing_Date_for_Applications
        self.Current_Closing_Date_for_Applications = Current_Closing_Date_for_Applications
        self.Archive_Date = Archive_Date
        self.Estimated_Total_Program_Funding = Estimated_Total_Program_Funding
        self.Award_Ceiling = Award_Ceiling
        self.Award_Floor = Award_Floor
    """

    def getAllIDs():
        #webdriver
        driver = webdriver.Chrome(executable_path="/gianyrox1/opt/anaconda3/lib/python3.9/site-packages")
        driver.implicitly_wait(10)
        driver.get(f"https://www.grants.gov/custom/search.jsp")

        pages = 104

        oppIds = []

        for i in tqdm(range(pages)):
            soups = BeautifulSoup(driver.page_source, features="lxml")

            hrefOppIds = []
            for a in soups.find_all('a', href=True):
                hrefOppIds.append(a['href'])

            javascriptOppIDs = []
            #get js viewOppDetails(oppID) calls
            for j in hrefOppIds:
                if 'viewOppDetails' in j:
                    javascriptOppIDs.append(j)

            #strip to get oppID and append to oppIDs
            for k in range(len(javascriptOppIDs)):
                oppIds.append(int(javascriptOppIDs[k].strip("javascript:viewOppDetails(").rstrip(", true)")))

            try:
                driver.find_element(By.LINK_TEXT, "Next »").click()
                time.sleep(10) #driver.implicitly_wait(10)
            except Exception as e:
                print(e)
                pass

        OppIDs = df(oppIds)
        OppIDs.to_csv('//Users//gianyrox1//bucket_projects//bucketGovGrants//OppIDs.csv', index=False)

        return oppIds

    def getNewIds():
        pass

    def getGrants():
        driver = webdriver.Chrome(executable_path="/gianyrox1/opt/anaconda3/lib/python3.9/site-packages")
        driver.implicitly_wait(10)

        newOpps = getNewIDs()

        oppIDs = list()
        nullIDs = []
        fullIDs = []

        for oppID in range(344637, 344650):

            ID = "oppId=" + str(oppID)

            oppIDString = "OppID" + str(oppID)

            driver.get(f"https://www.grants.gov/custom/viewOppDetails.jsp?{ID}")
            driver.execute_script("document.body.style.zoom='50%'")

            #check if ID is a grant
            ID_check = driver.find_element(By.ID, 'loadingDataMsg')
            if str(ID_check.text) == "There is no record found for your search.": 
                nullIDs.append(oppID)
                continue;
            
            
            fullIDs.append(oppID)

            synopsis = driver.find_elements(By.ID, 'synopsisDetailsContent')
        
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

            for value in pairs:
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
