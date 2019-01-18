'''
Action points:
- I get the limebikes information according to the reference; but, they are in unstructured format, and too cluttered. We need to create text (.csv) files for both bikes first.
- After that, we need them matched to GT coordinates
'''

# bikes and scooters might be mixed on limebikes, see json response and we would need to filter them
import requests
'''
params = (
    ('phone', '+14044524018'),
)

response = requests.get('https://web-production.lime.bike/api/rider/v1/login', params=params)
'''
headers = {
    'Content-Type': 'application/json',
}

data = '{"login_code": "696708", "phone": "+14044524018"}'

response = requests.post('https://web-production.lime.bike/api/rider/v1/login', headers=headers, data=data)
print(response.text)
print(response)
print(response.content)
print(str(response.cookies)[::-1])
