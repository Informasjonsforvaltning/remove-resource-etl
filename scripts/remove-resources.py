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
    return get_base_url(resource_type) + '/' + fdk_id + '/remove'


def get_base_url(resource_type):
    global env
    if resource_type in ['concepts', 'dataservices', 'datasets', 'events', 'informationmodels']:
        if env in ['staging', 'demo']:
            return 'https://' + resource_type + '.' + env + '.fellesdatakatalog.digdir.no/' + resource_type
        else:
            return 'https://' + resource_type + '.fellesdatakatalog.digdir.no/' + resource_type
    elif resource_type in ['public-services']:
        if env in ['staging', 'demo']:
            return 'https://services.' + env + '.fellesdatakatalog.digdir.no/' + resource_type
        else:
            return 'https://services.fellesdatakatalog.digdir.no/' + resource_type


resources = openfile(args.inputdirectory + 'remove_resources.json')
env_options = ['staging', 'demo', 'prod']
env = get_user_input("Please specify the environment where the script should be run (staging/demo/prod): ", env_options)
print(f"You have selected: {env}")

for resource in resources:
    if len(resources[resource]) > 0:
        removed = 0
        failed = 0
        print()
        print("Removing " + resource + ": ")
        for fdkId in resources[resource]:
            url = get_url(resource, fdkId)
            response = requests.request("POST", url=url, headers={"Authorization": "Bearer " + token})
            if response.status_code == 200:
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
