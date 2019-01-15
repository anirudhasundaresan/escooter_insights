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

# I will focus on getting the Bird bike data first.
import requests
import json

url = 'https://api.bird.co/user/login'

payload = {"email": "ihaadvr@g.com"}
headers = {'Device-id': '123e4567-e89b-12d3-a456-426655440000', 'Platform': 'ios', 'Content-type': 'application/json'}

r = requests.post(url, data=json.dumps(payload), headers=headers)
print(r.text) # this is a string! - not a dictionary
print(type(r.text))
# token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJBVVRIIiwidXNlcl9pZCI6Ijg0Yjk3N2RmLTM5MjMtNGM4NS1iYjc4LTM3OWI5MjYyNzAxNSIsImRldmljZV9pZCI6IjEyM2U0NTY3LWU4OWItMTJkMy1hNDU2LTQyNjY1NTQ0MDAwMCIsImV4cCI6MTU3OTA3NjkyOX0.iIXwWpyTngCWMyyyGjvPKdgmwaI1FuE1isucQx5lBiI"

token = json.loads(r.text)['token']
print(type(token))

'''

As I change any part of the payload, I get a new id and token.
This token has an expiry time, but this gets extended everytime you call the above. Your ID changes, but your token remains the same.

This token is what we will be using to get the location and data about the bikes.
'''

url_ = 'https://api.bird.co/bird/nearby?latitude=33.782678&longitude=-84.396896&radius=2000'
headers_ = {'Authorization': 'Bird {}'.format(token), 'Device-id': '123e4567-e89b-12d3-a456-426655440000', 'App-Version': '3.0.5', 'Location': '{"latitude":33.782678 ,"longitude":-84.396896,"altitude":500,"accuracy":100,"speed":-1,"heading":-1}'}
# see how altitude, accuracy, speed and heading matter?

r_ = requests.get(url_, headers=headers_)
print(r_)
print(json.loads(r_.content))

# see how you are going to manage data. 
