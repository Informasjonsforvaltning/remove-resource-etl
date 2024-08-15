import json
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputdirectory', help="the path to the directory of the input files", required=True)
args = parser.parse_args()
token_file_name = args.inputdirectory + '/token_file.txt'

env = input("Please specify the environment where the script should be run (staging/demo/prod): ")
while env not in ["staging", "demo", "prod"]:
    print("Incorrect environment value ...")
    env = input("Please specify the environment where the script should be run (staging/demo/prod): ")
with open(token_file_name, 'r') as token_file:
    token = token_file.read()


def openfile(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


def get_url(resource_type):
    global env
    if resource_type == 'concepts':
        if env in ['staging', 'demo']:
            return 'https://concepts.' + env + '.fellesdatakatalog.digdir.no/concepts/'
        else:
            return 'https://concepts.fellesdatakatalog.digdir.no/concepts/'
    elif resource_type == 'data-services':
        if env in ['staging', 'demo']:
            return 'https://dataservices.' + env + '.fellesdatakatalog.digdir.no/dataservices/'
        else:
            return 'https://dataservices.fellesdatakatalog.digdir.no/dataservices/'
    elif resource_type == 'datasets':
        if env in ['staging', 'demo']:
            return 'https://datasets.' + env + '.fellesdatakatalog.digdir.no/datasets/'
        else:
            return 'https://datasets.fellesdatakatalog.digdir.no/datasets/'
    elif resource_type == 'events':
        if env in ['staging', 'demo']:
            return 'https://' + env + '.fellesdatakatalog.digdir.no/events/'
        else:
            return 'https://data.norge.no/events/'
    elif resource_type == 'information-models':
        if env in ['staging', 'demo']:
            return 'https://informationmodels.' + env + '.fellesdatakatalog.digdir.no/informationmodels/'
        else:
            return 'https://informationmodels.fellesdatakatalog.digdir.no/informationmodels/'
    elif resource_type == 'services':
        if env in ['staging', 'demo']:
            return 'https://' + env + '.fellesdatakatalog.digdir.no/public-services/'
        else:
            return 'https://data.norge.no/public-services/'


resources = openfile(args.inputdirectory + 'resources.json')

for resource in resources:
    if len(resources[resource]) > 0:
        removed = 0
        failed = 0
        print()
        print("Removing " + resource + ": ")
        for fdkId in resources[resource]:
            url = get_url(resource) + fdkId
            response = requests.request("DELETE", url=url, headers={"Authorization": "Bearer " + token})
            if response.status_code == 204:
                removed += 1
                print('Resource ' + fdkId + ' removed successfully')
            elif response.status_code in [401, 403]:
                exit("The provided token was invalid or expired, exiting ...")
            else:
                failed += 1
                print(response.text)
        print('Removed ' + str(removed) + ' ' + resource + ' successfully')
        print('Failed to remove ' + str(failed) + ' ' + resource)

with open(token_file_name, 'w') as token_file:
    pass
