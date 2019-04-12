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
import json
import os
import sys
import time
import pprint
import requests
import webbrowser
# from PyQt5 import Qt
import mplleaflet
import networkx as nx
from random import randint
import pyscreenshot as ImageGrab
import matplotlib.pyplot as plt

i = 0
while True:
    url = 'https://api.bird.co/user/login'

    payload = {"email": "xfe" + "@vfdv.cm"}
    headers = {'Device-id': '123e4567-e89b-12d3-a456-426655440000', 'Platform': 'ios', 'Content-type': 'application/json'}

    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.text) # this is a string! - not a dictionary
    # print(type(r.text))

    token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJBVVRIIiwidXNlcl9pZCI6ImVjMThiZTdmLTI5YmEtNGYyZC04OGNjLTA5NTM1ZDhmYjE2NyIsImRldmljZV9pZCI6IjEyM2U0NTY3LWU4OWItMTJkMy1hNDU2LTQyNjY1NTQ0MDAwMCIsImV4cCI6MTU4NjM3NzAyOX0.aLzI3oGyhraK1swpa3Ew7saMrqW6Y-aKawOSXcZmIhQ"

    # token = json.loads(r.text)['token']
    # print(type(token))

    '''
    As I change any part of the payload, I get a new id and token.
    This token has an expiry time, but this gets extended everytime you call the above. Your ID changes, but your token remains the same.

    This token is what we will be using to get the location and data about the bikes.
    '''

    url_ = 'https://api.bird.co/bird/nearby?latitude=33.7746&longitude=-84.3973&radius=1000'
    # GT Tech Green coordinates given

    headers_ = {'Authorization': 'Bird {}'.format(token), 'Device-id': '123e4567-e89b-12d3-a456-426655440000', 'App-Version': '3.0.5', \
    'Location': '{"latitude":33.775620, "longitude":"-84.396286","altitude":500,"accuracy":100,"speed":-1,"heading":-1}'}
    # see how altitude, accuracy, speed and heading matter?

    r = requests.get(url_, headers=headers_)
    parsed_data = json.loads(r.text)

    for key in parsed_data:
        print("Key: ", key)

    print("Number of birds in this radius: ", len(parsed_data['birds']))
    print("Number of clusters: ", len(parsed_data['clusters']))
    print("Number of areas: ", len(parsed_data['areas']))

    temp = sys.stdout
    sys.stdout = open('birds_'+str(i)+'.csv', 'w')
    with open('birds_'+str(i)+'.csv', mode='w') as in_file:
        print("ID, Latitude, Longitude, Code, Captive, Battery_level \n")
        for id in parsed_data['birds']: # is a list
            print(id['id'], ',', id['location']['latitude'], ',', id['location']['longitude'], ',', id['code'], ',', id['captive'], ',', id['battery_level'], '\n')
    # see how you are going to manage data.
    sys.stdout.close() # ordinary file object
    sys.stdout = temp

    # making the graph
    G = nx.Graph()

    '''
    nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=5)
    plt.savefig(str(i) + '.png')
    plt.clf()
    time.sleep(0)
    '''


    color_map = [] # to play with battery percentages
    pos = {}
    fig, ax = plt.subplots()
    for bike in parsed_data['birds']:
        if bike['battery_level'] < 25:
            color_map.append('red')
        elif bike['battery_level'] < 50:
            color_map.append('orange')
        elif bike['battery_level'] < 75:
            color_map.append('blue')
        else:
            color_map.append('black')
        G.add_node(bike['id'], pos=(bike['location']['longitude'], bike['location']['latitude']))
        pos[bike['id']] = [bike['location']['longitude'], bike['location']['latitude']]
    nx.draw_networkx_nodes(G,pos=pos,node_size=9,edge_color='k',alpha=0.6, with_labels=False, node_color = color_map)
    # nx.draw_networkx_edges(G,pos=pos,edge_color='gray', alpha=.1)
    # nx.draw_networkx_labels(G,pos, label_pos =10.3)
    mplleaflet.show(fig=ax.figure)

    im_name = 'map_' + str(i) + '.png'
    fullpath = os.path.abspath('.')
    '''
    with open(fullpath, 'w') as f:
        save_html(fig, fileobj=f, **kwargs)
    '''
    webbrowser.open('file://' + fullpath + '/_map.html')
    # save an screenshot
    if (im_name):
        # wait for some seconds until map is ready

        # time.sleep(5)
        im = ImageGrab.grab(bbox=(80, 100, 1905, 1070)) # X1,Y1,X2,Y2
        im.show()
        im.save(fullpath + '/' + im_name)
        print("Screenshot saved at: "+ im_name)
        im.show()

    i += 1
    # time.sleep(12)
