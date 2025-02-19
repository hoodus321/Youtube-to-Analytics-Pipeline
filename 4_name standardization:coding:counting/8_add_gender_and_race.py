import os
import urllib.parse
from urllib.request import urlopen
import json
import csv

# Function to build the SPARQL query for multiple properties (gender, occupation, ethnic group)
def query_for_multiple_properties(person): 
    return urllib.parse.quote(
        "SELECT ?propLabel ?propertyLabel WHERE { " + 
        "SERVICE wikibase:label { bd:serviceParam wikibase:language \"[AUTO_LANGUAGE],en\". } " + 
        "{wd:" + person + " wdt:P21 ?property. " +  # Fetch P21 (gender)
        "?name ?ref wdt:P21. " + 
        "?name rdfs:label ?propLabel} " + 
        "UNION " + 
        "{wd:" + person + " wdt:P106 ?property. " +  # Fetch P106 (occupation)
        "?name ?ref wdt:P106. " + 
        "?name rdfs:label ?propLabel} " + 
        "UNION " + 
        "{wd:" + person + " wdt:P172 ?property. " +  # Fetch P172 (ethnic group)
        "?name ?ref wdt:P172. " + 
        "?name rdfs:label ?propLabel} " + 
        "FILTER((LANG(?propLabel)) = \"en\") " + 
        "} LIMIT 100", safe=""
    )

# Function to retrieve Wikidata information for a given entity (name)
def retrieve_wikidata(entity): 
    entity = entity.replace("\"", "").replace("—", "").replace("\\","")
    entity = entity.strip()
    url_prefix = "https://query.wikidata.org/sparql?format=json&query="
    query = urllib.parse.quote("SELECT ?item ?itemLabel WHERE {" + \
    "?item wdt:P31 wd:Q5." + \
    "?item ?label \"" + entity + "\"@en ." + \
    "SERVICE wikibase:label { bd:serviceParam wikibase:language \"en\". }" + \
    "}", safe='')
    print(f"Processing: {entity}")
    url = url_prefix + query
    try:
        res = json.loads(urlopen(url).read())
    except Exception as e:
        print(f"Error retrieving Wikidata for {entity}: {e}")
        return None
    
    cands = []
    if len(res['results']['bindings']) > 0:
        wikiID = res['results']['bindings'][0]['item']['value'].split('/')[-1]
        name = res['results']['bindings'][0]['itemLabel']['value'].split('/')[-1]
        person_dict = {}
        person_dict['name'] = name
        person_dict['wikiID'] = wikiID
        query_for_props = query_for_multiple_properties(wikiID)
        person_url = url_prefix + query_for_props
        try:
            response = urlopen(person_url)
            result = json.loads(response.read())
            for item in result['results']['bindings']: 
                label = item["propLabel"]["value"]
                prop_val = item["propertyLabel"]["value"]
                if label not in person_dict: 
                    person_dict[label] = [prop_val]
                else: 
                    person_dict[label].append(prop_val)
            cands.append(person_dict)
        except Exception as e:
            print(f"Error retrieving properties for {entity}: {e}")
            return None
    return cands[0] if cands else None

# Main function to process the input CSV and add new columns for gender, occupation, and ethnic group
def process_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['gender', 'occupation', 'ethnic_group']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in reader:
            entity = row['Name']
            wikidata_info = retrieve_wikidata(entity)
            
            # Default values if Wikidata info is not found
            gender = 'None'
            occupation = 'None'
            ethnic_group = 'None'
            
            if wikidata_info:
                gender = '|'.join(wikidata_info.get('sex or gender', ['None']))
                occupation = '|'.join(wikidata_info.get('occupation', ['None']))
                ethnic_group = '|'.join(wikidata_info.get('ethnic group', ['None']))
            
            # Write row to the output CSV
            row['gender'] = gender
            row['occupation'] = occupation
            row['ethnic_group'] = ethnic_group
            writer.writerow(row)

# Specify file paths here
input_file = 'famous_names_by_channel_{current_time}.csv'  # Replace with your input CSV file path
output_file = 'famous_names_by_channel_w_gender_and_race_{current_time}.csv'  # Replace with your desired output CSV file path

# Run the process
process_csv(input_file, output_file)
