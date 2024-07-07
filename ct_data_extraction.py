# This is the working code for extracting clinical trial data pertaining to Pfizer.
# This code will test the lambda function before loading into AWS.

# data_extraction.py

import requests
import pandas as pd

def extract_data():
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.spons": "Pfizer",
        "pageSize": 100
    }

    data_list = []

    while True:
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            studies = data.get('studies', [])

            for study in studies:
                nctId = study['protocolSection']['identificationModule'].get('nctId', 'Unknown')
                overallStatus = study['protocolSection']['statusModule'].get('overallStatus', 'Unknown')
                startDate = study['protocolSection']['statusModule'].get('startDateStruct', {}).get('date', 'Unknown Date')
                
                conditionsModule = study['protocolSection'].get('conditionsModule', {})
                conditions = ', '.join(conditionsModule.get('conditions', ['No conditions listed']))
                
                acronym = study['protocolSection']['identificationModule'].get('acronym', 'Unknown')
                interventions_list = study['protocolSection'].get('armsInterventionsModule', {}).get('interventions', [])
                interventions = ', '.join([intervention.get('name', 'No intervention name listed') for intervention in interventions_list]) if interventions_list else "No interventions listed"
                
                locations_list = study['protocolSection'].get('contactsLocationsModule', {}).get('locations', [])
                locations = ', '.join([f"{location.get('city', 'No City')} - {location.get('country', 'No Country')}" for location in locations_list]) if locations_list else "No locations listed"
                
                primaryCompletionDate = study['protocolSection']['statusModule'].get('primaryCompletionDateStruct', {}).get('date', 'Unknown Date')
                studyFirstPostDate = study['protocolSection']['statusModule'].get('studyFirstPostDateStruct', {}).get('date', 'Unknown Date')
                lastUpdatePostDate = study['protocolSection']['statusModule'].get('lastUpdatePostDateStruct', {}).get('date', 'Unknown Date')
                studyType = study['protocolSection']['designModule'].get('studyType', 'Unknown')
                phases = ', '.join(study['protocolSection']['designModule'].get('phases', ['Not Available']))

                data_list.append({
                    "NCT ID": nctId,
                    "Acronym": acronym,
                    "Overall Status": overallStatus,
                    "Start Date": startDate,
                    "Conditions": conditions,
                    "Interventions": interventions,
                    "Locations": locations,
                    "Primary Completion Date": primaryCompletionDate,
                    "Study First Post Date": studyFirstPostDate,
                    "Last Update Post Date": lastUpdatePostDate,
                    "Study Type": studyType,
                    "Phases": phases
                })

            nextPageToken = data.get('nextPageToken')
            if nextPageToken:
                params['pageToken'] = nextPageToken
            else:
                break
        else:
            print("Failed to fetch data. Status code:", response.status_code)
            break

    df = pd.DataFrame(data_list)
    return df
