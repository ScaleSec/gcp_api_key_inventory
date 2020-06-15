#!/usr/bin/env python

import requests
import json
import googleapiclient.discovery
import sys
import csv
import subprocess
import os
from flatten_json import flatten

def get_flattened_keys(projects):
    '''
    Transform an array of project-grouped keys into a list of flattened api key rows
    '''
    flat_keys = []

    for project in projects:
        for key_data in project:
            massage(key_data)
            flat_keys.append(flatten(key_data))

    return flat_keys

def massage(key_data):
    '''
    Does any custom flattening necessary for cleaner output.
    Called before passing the key dict to flatten()
    '''

    # collapse this map of keys to empty maps to just a list of strings
    if key_data.get("apiTargetKeyDetails"):
        targets = []
        for target in key_data["apiTargetKeyDetails"]["apiTargets"].keys():
            targets.append(target)
        key_data["apiTargetKeyDetails"] = ",".join(targets)

    return key_data

def unique_headers(keys):
    ''' Get the list of unique headers across all the flattened key dicts '''
    headers = {}
    for key_data in keys:
        for field in key_data:
            headers[field] = True
    return headers.keys()

def write_csv(api_keys):
    '''
    Constructs the keys into a csv file.
    This file can be used for reporting and analytics.
    '''

    headers = unique_headers(api_keys)

    with open('keys.csv', 'w') as key_csv:
        csv_writer = csv.writer(key_csv)
        csv_writer.writerow(headers)

        # Create our CSV rows using our API Key data.
        for key in api_keys:
            current_row = []
            for field in headers:
                current_row.append(key.get(field))
            csv_writer.writerow(current_row)

def get_keys():
    access_token = create_token()
    service = create_service()

    # List available projects
    request = service.projects().list()

    # Collect all the projects
    projects = []
    # Paginate through the list of all available projects
    while request is not None:
        response = request.execute()

        projects.extend(response.get('projects', []))

        request = service.projects().list_next(request, response)


    # This variable is used to hold our key JSON objects before we write to key_dump.json
    content = []
    # For each project, extract the project ID
    for project in projects:
        project_id = project['projectId']
        # Use the project ID and access token to find the API keys for each project
        keys = requests.get(
            f'https://apikeys.googleapis.com/v1/projects/{project_id}/apiKeys',
            params={'access_token': access_token}
        ).json()
        # Write Keys to a file for conversion
        if "error" not in keys: # Removes 403 permission errors from returning
            if keys:
                print(f"API Key found in project ID {project_id}.")
                content.append(keys['keys'])
            else:
                print(f"Project ID {project_id} has no API Keys.")

    return content

def create_token():
    '''
    There is no SDK for API Keys as of May 2020.
    We have to create a bearer token to submit with our HTTP requests in get_keys()
    You can create a token using google.auth.transport.requests.Request() but the scope requirement
    requires the official API to be activated and it is in early alpha / not available for most users.
    Check this URL for the API https://cloud.google.com/api-keys/docs/overview to know when it is public.
    '''
    access_token = subprocess.run('gcloud auth print-access-token', shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    token = access_token.stdout
    return token


def create_service():
    '''Creates the GCP Cloud Resource Service'''
    return googleapiclient.discovery.build('cloudresourcemanager', 'v1')


def main():
    project_keys = get_keys()

     # Writes our keys into a file
    with open('key_dump.json', 'w') as f:
        formatted = json.dumps(project_keys, indent=4, sort_keys=True)
        f.write(formatted)

    flat_keys = get_flattened_keys(project_keys)
    write_csv(flat_keys)

if __name__ == "__main__":
    main()
