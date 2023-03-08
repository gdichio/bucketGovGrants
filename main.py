import pandas as pd
from pandas import DataFrame
import src.Grants as G
from src.Grants import Grant
from src.OppsDB import Database
from src.Grants import getGrant
from src.Grants import oppCleaning


def main():

    oppIds = pd.read_csv('//Users//gianyrox1//bucket_projects//bucketGovGrants//OppIDs.csv')    

    OppDF = DataFrame()

    for oppId in oppIds:

        opp = DataFrame(getGrant(oppId))

        Opportunity = oppCleaning(opp)

        OppDF = pd.concat([OppDF,Opportunity], ignore_index=True)
        OppDF.to_csv('//Users//gianyrox1//bucket_projects//bucketGovGrants//OppDF.csv', index=False)
        
    df = pd.read_csv('//Users//gianyrox1//bucket_projects//bucketGovGrants//OppDF.csv', index=False)
    
    return df.head()

if __name__ == '__main__':
    main()