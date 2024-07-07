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
        if response.status_code != 200:
            print("Failed to fetch data. Status code:", response.status_code)
            break

        data = response.json()
        studies = data.get('studies', [])

        for study in studies:
            protocol_section = study.get('protocolSection', {})
            identification_module = protocol_section.get('identificationModule', {})
            status_module = protocol_section.get('statusModule', {})
            conditions_module = protocol_section.get('conditionsModule', {})
            arms_interventions_module = protocol_section.get('armsInterventionsModule', {})
            contacts_locations_module = protocol_section.get('contactsLocationsModule', {})
            design_module = protocol_section.get('designModule', {})

            nctId = identification_module.get('nctId', 'Unknown')
            overallStatus = status_module.get('overallStatus', 'Unknown')
            startDate = status_module.get('startDateStruct', {}).get('date', 'Unknown Date')
            conditions = ', '.join(conditions_module.get('conditions', ['No conditions listed']))
            acronym = identification_module.get('acronym', 'Unknown')

            interventions_list = arms_interventions_module.get('interventions', [])
            interventions = ', '.join([intervention.get('name', 'No intervention name listed') for intervention in interventions_list]) if interventions_list else "No interventions listed"

            locations_list = contacts_locations_module.get('locations', [])
            locations = ', '.join([f"{location.get('city', 'No City')} - {location.get('country', 'No Country')}" for location in locations_list]) if locations_list else "No locations listed"

            primaryCompletionDate = status_module.get('primaryCompletionDateStruct', {}).get('date', 'Unknown Date')
            studyFirstPostDate = status_module.get('studyFirstPostDateStruct', {}).get('date', 'Unknown Date')
            lastUpdatePostDate = status_module.get('lastUpdatePostDateStruct', {}).get('date', 'Unknown Date')
            studyType = design_module.get('studyType', 'Unknown')
            phases = ', '.join(design_module.get('phases', ['Not Available']))

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
        if not nextPageToken:
            break
        params['pageToken'] = nextPageToken

    df = pd.DataFrame(data_list)
    return df
