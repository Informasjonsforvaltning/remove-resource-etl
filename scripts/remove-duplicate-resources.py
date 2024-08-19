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


def get_url(resource_type):
    global env
    if resource_type in ['concepts', 'dataservices', 'datasets', 'informationmodels']:
        if env in ['staging', 'demo']:
            return 'https://' + resource_type + '.' + env + '.fellesdatakatalog.digdir.no/' + resource_type + '/duplicates'
        else:
            return 'https://' + resource_type + '.fellesdatakatalog.digdir.no/' + resource_type + '/duplicates'
    elif resource_type in ['events', 'public-services']:
        if env in ['staging', 'demo']:
            return 'https://' + env + '.fellesdatakatalog.digdir.no/' + resource_type + '/duplicates'
        else:
            return 'https://data.norge.no/' + resource_type + '/duplicates'


duplicate_resources = openfile(args.inputdirectory + 'duplicate_resources.json')
env_options = ['staging', 'demo', 'prod']
env = get_user_input("Please specify the environment where the script should be run (staging/demo/prod): ", env_options)
print(f"You have selected: {env}")

for resource_type in duplicate_resources:
    if len(duplicate_resources[resource_type]) > 0:
        print()
        print("Removing duplicate " + resource_type + ": ")
        url = get_url(resource_type)
        response = requests.request("POST", url=url, json=duplicate_resources[resource_type], headers={"Authorization": "Bearer " + token})
        if response.status_code == 200:
            print('Duplicate resources removed successfully!')
        elif response.status_code in [401, 403]:
            exit("The provided token was invalid or expired, exiting ...")
        else:
            print("There was an error while removing duplicate " + resource_type + " ...")
            print(response.text)
            with open(args.inputdirectory + 'failed_response.json', 'w') as error_file:
                error_file.write(response.text)

with open(token_file_name, 'w') as token_file:
    pass
