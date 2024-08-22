import json
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputdirectory', help="the path to the directory of the input files", required=True)
args = parser.parse_args()
token_file_name = args.inputdirectory + '/token_file.txt'
with open(token_file_name, 'r') as token_file:
    token = token_file.read()


def get_user_input(prompt, valid_options):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        print(f"Invalid input. Please enter one of the following options: {', '.join(valid_options)}")


def openfile(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


def get_url(resource_type, fdk_id):
    global env
    if resource_type in ['concepts', 'dataservices', 'datasets', 'events', 'informationmodels']:
        if env in ['staging', 'demo']:
            return 'https://' + resource_type + '.' + env + '.fellesdatakatalog.digdir.no/' + resource_type + '/' + fdk_id
        else:
            return 'https://' + resource_type + '.fellesdatakatalog.digdir.no/' + resource_type + '/' + fdk_id
    elif resource_type in ['public-services']:
        if env in ['staging', 'demo']:
            return 'https://services.' + env + '.fellesdatakatalog.digdir.no/' + resource_type + '/' + fdk_id
        else:
            return 'https://services.fellesdatakatalog.digdir.no/' + resource_type + '/' + fdk_id


def get_resource_service_url(resource_type, fdk_id):
    global env
    if resource_type == 'dataservices':
        resource_type = 'data-services'
    elif resource_type == 'informationmodels':
        resource_type = 'information-models'
    elif resource_type == 'public-services':
        resource_type = 'services'
    if env in ['staging', 'demo']:
        return 'https://resource.api.' + env + '.fellesdatakatalog.digdir.no/' + resource_type + '/' + fdk_id
    else:
        return 'https://resource.api.fellesdatakatalog.digdir.no/' + resource_type + '/' + fdk_id


resources_to_purge = openfile(args.inputdirectory + 'purge_resources.json')
env_options = ['staging', 'demo', 'prod']
env = get_user_input("Please specify the environment where the script should be run (staging/demo/prod): ", env_options)
print(f"You have selected: {env}")

for resource in resources_to_purge:
    if len(resources_to_purge[resource]) > 0:
        removed_rdf = 0
        removed_json = 0
        failed_rdf = 0
        failed_json = 0
        print()
        print("Purging " + resource + ": ")
        for fdkId in resources_to_purge[resource]:
            url = get_url(resource, fdkId)
            resource_api_url = get_resource_service_url(resource, fdkId)
            response_rdf = requests.request("DELETE", url=url, headers={"Authorization": "Bearer " + token})
            response_json = requests.request("DELETE", url=resource_api_url, headers={"Authorization": "Bearer " + token})
            if response_rdf.status_code == 204:
                removed_rdf += 1
                print('RDF: Resource ' + fdkId + ' purge job accepted')
            elif response_rdf.status_code in [401, 403]:
                exit("RDF: The provided token was invalid or expired, exiting ...")
            else:
                failed_rdf += 1
                print('RDF failed, status: ' + str(response_rdf.status_code))
            if response_json.status_code == 204:
                removed_json += 1
                print('JSON: Resource ' + fdkId + ' purged successfully')
            elif response_json.status_code in [401, 403]:
                exit("JSON: The provided token was invalid or expired, exiting ...")
            else:
                failed_json += 1
                print('JSON failed, status: ' + str(response_json.status_code))
        print(resource + ': RDF purge jobs accepted: ' + str(removed_rdf) + ' || Purged JSON: ' + str(removed_json))
        print(resource + ': RDF purge jobs not accepted: ' + str(failed_rdf) + ' || Failed to purge JSON: ' + str(failed_json))

with open(token_file_name, 'w') as token_file:
    pass
