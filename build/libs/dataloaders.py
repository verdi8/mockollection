import json
import string

import requests


def load_wikidata_sparql_data(query_file_path : str, lang : str):
    """
    Loads data from the Wikidata SPARQL service.
    More info here : https://www.mediawiki.org/wiki/Wikidata_Query_Service/User_Manual#SPARQL_endpoint
    """
    # Reads the query from the file as a string.Template
    with open(query_file_path) as query_file:
        query_template = string.Template(query_file.read().replace("\r", ""))
        query = query_template.substitute(lang=lang)

    # Calls the Wikidata SPARQL service
    params = {
        "query" : query,
        "format" : "json"
    }
    response = requests.get('https://query.wikidata.org/sparql', params)
    response.raise_for_status()

    json_response = json.loads(response.text)

    # Converts the SPARQL json_response into simplified dict
    # See https://www.w3.org/TR/2013/REC-sparql11-results-json-20130321/
    vars = json_response["head"]["vars"]

    id = 0;

    data = []
    for binding in json_response["results"]["bindings"] :
        item = {}

        for var in vars :
            value = binding[var]["value"]
            item[var] = value

        data.append(item)
    return data
