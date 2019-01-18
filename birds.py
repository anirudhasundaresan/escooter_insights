'''
References:
http://conormclaughlin.net/2018/08/tracking-the-flow-of-bird-scooters-across-dc/#obtaining-api-access
https://github.com/ubahnverleih/WoBike/blob/master/Lime.md
https://github.com/ubahnverleih/WoBike/blob/master/Bird.md

Obtaining API acess:
- “Log in” to the Bird API and receive an authentication token
- Retrieve a listing all Bird scooters in the DC area with their location, unique ID, and battery level
- Write the listing to a CSV
'''

# Birds are available only between 4AM - 9PPM.
# I will focus on getting the Bird bike data first.
import requests
import json
from random import randint
import pprint

url = 'https://api.bird.co/user/login'

# str(randint(0,900))

payload = {"email": "ife" + "@vfdv.cm"}
headers = {'Device-id': '123e4567-e89b-12d3-a456-426655440000', 'Platform': 'ios', 'Content-type': 'application/json'}

r = requests.post(url, data=json.dumps(payload), headers=headers)
# print(r.text) # this is a string! - not a dictionary
# print(type(r.text))

token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJBVVRIIiwidXNlcl9pZCI6ImM5YTVlNzM2LWRlMjctNGFkNy1hMGI2LTA2OWZkMWJhN2YzMyIsImRldmljZV9pZCI6IjEyM2U0NTY3LWU4OWItMTJkMy1hNDU2LTQyNjY1NTQ0MDkwMCIsImV4cCI6MTU3OTMzMjA1NH0.-LA0hg3gr9hPKXKLrvSPbElggWrJjDZDWUpPXJmGWhw"

# token = json.loads(r.text)['token']
# print(type(token))

'''
As I change any part of the payload, I get a new id and token.
This token has an expiry time, but this gets extended everytime you call the above. Your ID changes, but your token remains the same.

This token is what we will be using to get the location and data about the bikes.
'''

url_ = 'https://api.bird.co/bird/nearby?latitude=33.775620&longitude=-84.396286&radius=00.0000111'
headers_ = {'Authorization': 'Bird {}'.format(token), 'Device-id': '123e4567-e89b-12d3-a456-426655440000', 'App-Version': '3.0.5', \
'Location': '{"latitude":33.775620, "longitude":"-84.396286","altitude":500,"accuracy":100,"speed":-1,"heading":-1}'}
# see how altitude, accuracy, speed and heading matter?

r = requests.get(url_, headers=headers_)
# print(r)
parsed_data = json.loads(r.text)

'''
for key in parsed_data:
    print("Key: ", key)

print("Under key=birds: ", parsed_data['birds'], " and number of birds in this radius: ", len(parsed_data['birds']))
print("Under key=clusters", parsed_data['clusters'], "and number of clusters: ", len(parsed_data['clusters']))
print("Under key=areas", parsed_data['areas'], "and number of areas: ", len(parsed_data['areas']))
'''
'''
with open('birds.csv', mode='w') as in_file:
    print("ID, Latitude, Longitude, Code, Captive, Battery_level \n")
    for id in parsed_data['birds']: # is a list
        print(id['id'], ',', id['location']['latitude'], ',', id['location']['longitude'], ',', id['code'], ',', id['captive'], ',', id['battery_level'], '\n')
# see how you are going to manage data.
'''

ls = []
# check if the ids from these bikes are all unique, and that each id represents the same bike.
for id in parsed_data['birds']:
    ls.append(id['id'])
print(len(ls))
ls.sort()
print(ls)
